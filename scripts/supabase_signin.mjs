const SUP_URL = process.env.SUPABASE_URL || 'https://dhbgmwkvoxnjzyskthba.supabase.co';
const SUP_ANON = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRoYmdtd2t2b3huanp5c2t0aGJhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwMzQ4NjksImV4cCI6MjA3NTYxMDg2OX0.kqxV3hbYDTo-fQQhXqp1OziB0bBymAqhDJn97s6piy0';
const EMAIL = process.env.TEST_EMAIL || 'test@risko.com';
const PASSWORD = process.env.TEST_PASSWORD || 'password123';

async function run(){
  try{
    const mod = await import('@supabase/supabase-js');
    const { createClient } = mod;
    const supabase = createClient(SUP_URL, SUP_ANON);
    const { data, error } = await supabase.auth.signInWithPassword({ email: EMAIL, password: PASSWORD });
    console.log(JSON.stringify({ data, error }, null, 2));
  }catch(e){
    console.error('ERR', e && e.stack ? e.stack : e);
    process.exitCode = 2;
  }
}

run();
