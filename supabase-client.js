// Lightweight helper to initialize and use Supabase Auth from the frontend
(function(){
  const CFG = window.RISKO_CONFIG || { API_BASE_URL: '' };
  const state = {
    enabled: false,
    initialized: false,
    initPromise: null,
  };

  async function fetchAuthConfig(){
    const url = `${CFG.API_BASE_URL}/api/v1/auth/config`;
    try {
      const res = await fetch(url);
      if (!res.ok) return null;
      return await res.json();
    } catch { return null; }
  }

  async function exchangeFromUrl(client){
    // Support hash params (access_token) or code exchange
    const hash = window.location.hash || '';
    const params = new URLSearchParams(hash.replace(/^#/, ''));
    const access_token = params.get('access_token');
    const refresh_token = params.get('refresh_token');
    if (access_token && refresh_token) {
      await client.auth.setSession({ access_token, refresh_token });
      return;
    }
    const search = new URLSearchParams(window.location.search);
    const code = search.get('code');
    if (code && typeof client.auth.exchangeCodeForSession === 'function') {
      try { await client.auth.exchangeCodeForSession({ code }); } catch {}
    }
  }

  async function init(){
    if (state.initPromise) return state.initPromise;
    state.initPromise = (async () => {
      const cfg = await fetchAuthConfig();
      if (!cfg || cfg.auth_provider !== 'supabase' || !cfg.supabase_url || !cfg.supabase_anon_key) {
        state.enabled = false;
        state.initialized = true;
        return false;
      }
      if (typeof window.supabase === 'undefined' || !window.supabase?.createClient) {
        console.warn('Supabase JS not loaded; include @supabase/supabase-js v2 script.');
        state.enabled = false;
        state.initialized = true;
        return false;
      }
      const client = window.supabase.createClient(cfg.supabase_url, cfg.supabase_anon_key);
      state.client = client;
      await exchangeFromUrl(client);
      state.enabled = true;
      state.initialized = true;
      return true;
    })();
    return state.initPromise;
  }

  async function getToken(){
    if (!state.initialized) await init();
    if (!state.enabled) return null;
    const { data } = await state.client.auth.getSession();
    return data?.session?.access_token || null;
  }

  async function handleAuthStateChange(event, session) {
    const analysisHistorySection = document.getElementById('analysis-history');
    const historyContainer = document.getElementById('history-container');

    if (event === 'SIGNED_IN') {
      analysisHistorySection.style.display = 'block';
      const token = session.access_token;
      try {
        const response = await fetch(`${CFG.API_BASE_URL}/api/v1/analyses/me`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          const analyses = await response.json();
          historyContainer.innerHTML = '';
          if (analyses.length === 0) {
            historyContainer.innerHTML = '<p>Daha önce hiç analiz yapmadınız.</p>';
          } else {
            analyses.forEach(analysis => {
              const item = document.createElement('div');
              item.className = 'list-group-item';
              item.innerHTML = `
                <h5>${analysis.address}</h5>
                <p>Risk Skoru: ${analysis.overall_risk_score || 'N/A'}</p>
                <small>${new Date(analysis.created_at).toLocaleString()}</small>
              `;
              historyContainer.appendChild(item);
            });
          }
        } else {
          console.error('Failed to fetch analyses:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching analyses:', error);
      }
    } else if (event === 'SIGNED_OUT') {
      analysisHistorySection.style.display = 'none';
      historyContainer.innerHTML = '';
    }
  }

  window.RiskoAuth = {
    get enabled(){ return state.enabled; },
    init,
    async login(email, password){
      await init();
      if (!state.enabled) throw new Error('Supabase not enabled');
      const { data, error } = await state.client.auth.signInWithPassword({ email, password });
      if (error) throw error;
      return data;
    },
    async register(name, email, password){
      await init();
      if (!state.enabled) throw new Error('Supabase not enabled');
      const { data, error } = await state.client.auth.signUp({
        email,
        password,
        options: { data: { name } }
      });
      if (error) throw error;
      return data;
    },
    async requestPasswordReset(email, redirectTo){
      await init();
      if (!state.enabled) throw new Error('Supabase not enabled');
      const redirect = redirectTo || `${window.location.origin}${window.location.pathname.replace(/[^/]*$/, '')}reset.html`;
      const { data, error } = await state.client.auth.resetPasswordForEmail(email, { redirectTo: redirect });
      if (error) throw error;
      return data;
    },
    async updatePassword(newPassword){
      await init();
      if (!state.enabled) throw new Error('Supabase not enabled');
      const { data, error } = await state.client.auth.updateUser({ password: newPassword });
      if (error) throw error;
      return data;
    },
    getToken,
  };

  // Attach the listener to Supabase auth state changes
  state.client.auth.onAuthStateChange(handleAuthStateChange);
})();
