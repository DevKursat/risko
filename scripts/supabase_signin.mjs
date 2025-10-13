const SUP_URL = process.env.SUPABASE_URL || '';
const SUP_ANON = process.env.SUPABASE_ANON_KEY || '';
const EMAIL = process.env.TEST_EMAIL || 'test@risko.com';
const PASSWORD = process.env.TEST_PASSWORD || 'password123';

async function run(){
  try{
    const mod = await import('@supabase/supabase-js');
    const { createClient } = mod;
    if (!SUP_URL || !SUP_ANON) {
      console.error('SUPABASE_URL or SUPABASE_ANON_KEY not set in environment; aborting.');
      process.exitCode = 2;
      return;
    }
    const supabase = createClient(SUP_URL, SUP_ANON);
    const { data, error } = await supabase.auth.signInWithPassword({ email: EMAIL, password: PASSWORD });
    console.log(JSON.stringify({ data, error }, null, 2));
  }catch(e){
    console.error('ERR', e && e.stack ? e.stack : e);
    process.exitCode = 2;
  }
}

run();
