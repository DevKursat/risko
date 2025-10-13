// Lightweight helper to initialize and use Supabase Auth from the frontend
(function(){
  const CFG = window.RISKO_CONFIG || { API_BASE_URL: '' };
  const state = {
    enabled: false,
    initialized: false,
    initPromise: null,
  };

  async function fetchAuthConfig(){
      // Prefer configuration passed from the page (window.RISKO_CONFIG).
      // For GitHub Pages, set RISKO_CONFIG in `config.js` to include supabase_url and supabase_anon_key.
      const pageCfg = (window.RISKO_CONFIG && typeof window.RISKO_CONFIG === 'object') ? window.RISKO_CONFIG : {};
      if (pageCfg.auth_provider === 'supabase' && pageCfg.supabase_url && pageCfg.supabase_anon_key) {
        return {
          auth_provider: 'supabase',
          supabase_url: pageCfg.supabase_url,
          supabase_anon_key: pageCfg.supabase_anon_key,
        };
      }

      // No public config found. Do not return a secret from the repo.
      console.warn('Supabase configuration not found in window.RISKO_CONFIG; Supabase auth disabled for safety.');
      return null;
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

  window.RiskoAuth = {
    get enabled(){ return state.enabled; },
    init,
    async login(email, password){
      await init();
      if (!state.enabled) throw new Error('Supabase not enabled');
      const { data, error } = await state.client.auth.signInWithPassword({ email, password });
      if (error) {
        console.error('Supabase login error:', error);
        const msg = (error.status ? `${error.status} ` : '') + (error.message || JSON.stringify(error));
        throw new Error(msg);
      }
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
      if (error) {
        console.error('Supabase register error:', error);
        const msg = (error.status ? `${error.status} ` : '') + (error.message || JSON.stringify(error));
        throw new Error(msg);
      }
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
})();
