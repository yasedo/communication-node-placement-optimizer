# Projeyi anlamak: haberleşme noktalarının yerleşimi

## Bir cümlede ne yapıyor?

Hayali bir haritaya yerleştirilen beş cihazın konumunu değiştirip daha çok kareyi kapsayan bir yerleşim arıyor.

Bu ilk sürüm yalnızca geometrik kapsama hesabı yapıyor. Cihazların birbiriyle haberleşip haberleşmediğini veya gerçek sinyal gücünü hesaplamıyor.

## Haritayı nasıl okuyacağım?

Harita 30 × 30 = 900 hücre. Gri dikdörtgenlerde cihaz yerleştirmiyoruz ve bu hücreleri hedef alana dahil etmiyoruz. Geriye 846 hedef hücre kalıyor. Mavi hücreler en az bir cihazın kapsama çemberinin içinde, krem hücreler dışında. Koyu noktalar cihazlar; etraflarındaki çemberlerin yarıçapı altı harita birimi.

Gri alanlar duvar veya dağ gibi sinyali kesmiyor. Bu sürümde fiziksel engel modeli yok. Harita birimi de doğrudan metre demek değil.

## Skor ne?

Skor = kapsanan hedef hücre sayısı / toplam hedef hücre sayısı.

Başlangıçta 367 / 846 = %43.38. Sonuçta 534 / 846 = %63.12.

Artış 19.74 **yüzde puanı**. Bu ifade, göreli yüzde artışla aynı şey değildir. Bir hücre iki cihazın kapsamasında olsa bile bir kez sayılıyor. Dolayısıyla çemberleri üst üste yığmak çoğu zaman alanı boşa harcıyor.

## Algoritma nasıl düşünüyor?

1. Geçerli bir rastgele başlangıç oluşturuyor.
2. Bir cihaz seçiyor.
3. Genellikle yakına, bazen daha uzaktaki izinli bir konuma taşımayı deniyor.
4. Yeni kapsama skorunu hesaplıyor.
5. Skor daha iyiyse yeni yerleşimi koruyor; değilse eskiyi tutuyor.
6. Bu işlemi 1.500 kez tekrarlıyor.

Bunun adı stokastik tepe tırmanışı, İngilizcesi stochastic hill climbing. Stokastik, aday hamlelerin rastgele seçildiği anlamına geliyor. Algoritma hiçbir zaman bildiği en iyi skoru kötüleştirmiyor, ama bu her zaman dünyanın en iyi yerleşimini bulduğu anlamına gelmiyor.

Bu sürümde genetik algoritma, pekiştirmeli öğrenme veya eğitilmiş bir yapay zekâ modeli yok. Başvuruda yöntemi bu adıyla anlat.

## Seed neden var?

Seed rastgele sayı üretecinin başlangıç ayarı. Aynı kod, aynı kütüphaneler ve aynı seed ile aynı deneyi yeniden üretmek için kullanılıyor. Cihazlar için 42, yerleşimi iyileştirmek için 43, rastgele karşılaştırma için 44 kullanılıyor. Seed değiştirilirse başlangıç ve sonuç değişebilir.

## Karşılaştırma neden gerekli?

Sadece kötü bir başlangıç seçip sonucu iyileştirmek güçlü bir yöntem kanıtı değil. Bu nedenle ikinci bir yöntem, 1.500 tamamen rastgele yerleşim üretiyor ve en iyisini seçiyor. İki yöntemde de başlangıç dahil 1.501 skor değerlendirmesi var. Geçersiz hamle de deneme bütçesinden sayılıyor.

Varsayılan deneyde tepe tırmanışı %63.12, rastgele arama %58.16. Beş farklı başlangıç için de `benchmark.csv` var. Bunlar küçük örnek deneyler; tüm haritalarda üstünlük kanıtlamıyor.

## Dosyaları nereden inceleyeceğim?

`main.py` içindeki `make_terrain` haritayı, `coverage_mask` kapsama hücrelerini, `coverage_score` skoru, `optimize` iyileştirme döngüsünü, `random_search` karşılaştırmayı, `plot_results` grafikleri hazırlıyor.

`results/node_positions.csv` gerçek başlangıç ve sonuç koordinatlarını içeriyor. `results/summary.json` koşulları ve skorları, `convergence.csv` her adımda bilinen en iyi skoru gösteriyor. Grafikler bu çalıştırmadan üretildi.

## Sınırları nasıl anlatacağım?

Gerçek radyo yayılımı, arazi yüksekliği, görüş hattı, girişim, cihaz enerjisi, veri aktarım hızı ve cihazlar arası bağlantı yok. Kapsama skorunun iyi olması, gerçek bir haberleşme ağının iyi çalışacağını göstermiyor.

Geliştirmek için önce farklı algoritmaları karşılaştırmak, sonra bağlantı kısıtı ve fiziksel yayılım modelini eklemek gerekir. Bu özellikleri şimdiden yaptığını söyleme.

## Sorulursa neyi doğru şekilde söyleyebilirim?

Yazılım deneyiminin sınırlı olduğunu, yapay zekâ yardımıyla hazırlanan bir başlangıç prototipini inceleyerek öğrenmeye başladığını söyle. Kodu tek başına yazdığını, makine öğrenmesi modeli eğittiğini veya gerçek sahada test yaptığını söyleme. Bu notları okuduktan ve bir çalıştırmayı gördükten sonra yöntemi kendi sözlerinle açıklamaya çalış.

Anlama kontrolü: Çemberler niçin fazla örtüşmesin? Seed ne işe yarıyor? Gri alanlar sinyali engelliyor mu? %63.12 gerçek telsiz başarısını ölçüyor mu? En iyi mümkün sonucu bulduğumuzu kanıtladık mı? Bu sorulara açıklama yapabiliyorsan prototipin temel mantığını anlamışsındır.
