-- Bu SQL betiği, Risko projesi için yapılan analizlerin kaydedileceği
-- 'analyses' tablosunu ve gerekli güvenlik kurallarını oluşturur.
-- Supabase SQL Editor'e yapıştırıp çalıştırabilirsiniz.

-- 1. 'analyses' tablosunu oluşturma
CREATE TABLE public.analyses (
  -- Benzersiz birincil anahtar (UUID)
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Analizi yapan kullanıcının ID'si. auth.users tablosuna bağlıdır.
  -- Kullanıcı silinirse bu alan NULL olur, analiz kaydı silinmez.
  -- Anonim analizler için bu alan NULL olabilir.
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,

  -- Analiz edilen adres bilgisi
  address TEXT NOT NULL,

  -- Analiz sonucunda dönen skorları içeren JSON verisi
  risk_scores JSONB NOT NULL,

  -- Kaydın oluşturulma zamanı (otomatik olarak ayarlanır)
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Tablo için açıklayıcı bir yorum ekleme
COMMENT ON TABLE public.analyses IS 'Kullanıcıların yaptığı risk analizi sonuçlarını saklar.';

-- 2. Satır Seviyesi Güvenlik (Row Level Security - RLS)
-- BU ADIM ÇOK ÖNEMLİDİR! Kullanıcıların sadece kendi verilerine erişmesini sağlar.
ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;

-- 3. Güvenlik Politikaları (Policies)

-- SELECT (Okuma) Politikası:
-- Bu kural, giriş yapmış bir kullanıcının SADECE kendi 'user_id'sine sahip
-- analiz kayıtlarını görmesine izin verir.
CREATE POLICY "Kullanıcılar yalnızca kendi analizlerini görebilir"
ON public.analyses
FOR SELECT
USING (auth.uid() = user_id);

-- INSERT (Ekleme) Politikası:
-- Bu kural, bir kullanıcının ya kendi 'user_id'si ile ya da anonim olarak
-- (user_id'yi NULL bırakarak) yeni bir analiz kaydı eklemesine izin verir.
CREATE POLICY "Kullanıcılar analiz ekleyebilir"
ON public.analyses
FOR INSERT
WITH CHECK ((auth.uid() = user_id) OR (user_id IS NULL));

-- Not: UPDATE ve DELETE politikaları eklenmemiştir.
-- MVP aşamasında analiz kayıtlarının güncellenmesi veya silinmesi
-- beklenmediği için bu işlemler varsayılan olarak engellenmiştir.
