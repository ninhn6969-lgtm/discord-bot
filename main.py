import os
import json
import random
import requests
import discord
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
from keep_alive import keep_alive # Đã thêm dòng này

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")

WEATHER_API = "16dd80ccb3b2e13098744cad826085b2"
CHANNEL_ID = 1437653177846599852

cities = [
    ("Hà Nội", "Hanoi"),
    ("Hạ Long", "Ha Long"),
    ("Thanh Hóa", "Thanh Hoa"),
    ("TP.HCM", "Ho Chi Minh City")
]

morning_messages = [
    "🔥 Hôm nay hãy cố gắng hết mình nhé!",
    "☀️ Chúc mọi người một ngày tuyệt vời!",
    "😎 Đừng quên uống đủ nước trong ngày nhé!",
    "💪 Hôm nay là một cơ hội mới — hãy tận dụng nó!",
    "🌸 Chúc mọi người luôn vui vẻ và tràn đầy năng lượng!",
    "🚀 Tiến lên nào, một ngày mới đang chờ bạn!",
    "🎮 Chúc bạn có những khoảnh khắc vui vẻ hôm nay!",
    "📚 Học tập thật tốt, thành công sẽ đến!",
    "🌈 Một ngày đẹp trời đang chờ bạn khám phá!",
    "⭐ Hãy luôn mỉm cười, cuộc sống sẽ tươi đẹp hơn!",
    "🍀 Chúc bạn gặp nhiều may mắn hôm nay!",
    "🔥 Never give up — hôm nay bạn sẽ làm được!",
    "🎵 Chúc bạn một ngày đầy âm nhạc và niềm vui!",
    "🌻 Hãy bắt đầu ngày mới với nụ cười thật tươi!",
    "💡 Mỗi buổi sáng là một trang giấy trắng — hãy viết thật đẹp!",
    "🏃 Hôm nay hãy vận động một chút để cơ thể khỏe mạnh!",
    "🍵 Uống ly trà/cà phê sáng và bắt đầu ngày mới nào!",
    "🌅 Bình minh mới, cơ hội mới — hãy nắm lấy!",
    "💬 Hãy nói một điều tốt đẹp với người thân hôm nay!",
    "🎯 Hôm nay hãy tập trung vào mục tiêu của bạn!",
    "🧘 Hít thở sâu, giữ bình tĩnh và làm việc thật hiệu quả!",
    "🌿 Một ngày xanh mát đang chờ bạn — hãy tận hưởng!",
    "🦋 Hôm nay sẽ là một ngày tuyệt vời, mình cảm nhận được!",
    "💎 Bạn đặc biệt hơn bạn nghĩ — hãy tin vào bản thân!",
    "🎊 Chúc mừng một ngày mới! Hãy làm cho nó đáng nhớ!",
    "🌍 Thế giới đang chờ bạn chinh phục — bắt đầu từ hôm nay!",
    "🏆 Người chiến thắng luôn bắt đầu ngày mới với thái độ tích cực!",
    "🌟 Hôm nay hãy là phiên bản tốt hơn của chính mình!",
    "🍎 Ăn sáng đầy đủ để có năng lượng cho cả ngày nhé!",
    "🎶 Một giai điệu vui tươi cho buổi sáng của bạn!",
    "🌞 Mặt trời đã mọc — đã đến lúc tỏa sáng rồi!",
    "💌 Gửi đến mọi người một buổi sáng đầy yêu thương!",
    "🧡 Hôm nay hãy làm điều gì đó khiến bạn hạnh phúc!",
    "🌺 Chúc buổi sáng tươi đẹp như những bông hoa!",
    "🛡️ Hôm nay dù khó khăn thế nào, bạn cũng sẽ vượt qua được!",
    "🎠 Cuộc sống thật thú vị — hãy tận hưởng từng khoảnh khắc!",
    "🦁 Dũng cảm lên! Ngày hôm nay là của bạn!",
    "🌊 Hãy để năng lượng tích cực lan tỏa xung quanh bạn!",
    "🎁 Mỗi ngày là một món quà — hãy trân trọng nó!",
    "🍓 Chúc buổi sáng ngọt ngào như những quả dâu tây!",
    "🔮 Ngày hôm nay chứa đựng những điều kỳ diệu đang chờ bạn!",
    "🌈 Sau mưa trời lại sáng — hãy luôn hy vọng!",
    "💫 Bạn có thể làm được bất cứ điều gì bạn quyết tâm!",
    "🏄 Hãy lướt qua ngày hôm nay với nụ cười trên môi!",
    "🌙 Đêm qua đã qua, hôm nay là ngày mới tươi sáng hơn!",
    "🎤 Hãy nói lên những điều bạn muốn và theo đuổi ước mơ!",
    "🌸 Xuân trong lòng mỗi ngày khi bạn sống lạc quan!",
    "🏔️ Leo cao hơn mỗi ngày — từng bước nhỏ sẽ tạo nên thành công lớn!",
    "🎨 Hôm nay hãy sáng tạo và làm điều gì đó mới mẻ!",
    "🦅 Bay cao hơn nhé — bầu trời là giới hạn của bạn!",
    "🌻 Hướng về phía mặt trời — bóng tối sẽ ở phía sau!",
    "💪 Sức mạnh không đến từ những gì bạn làm được, mà từ việc vượt qua những gì bạn tưởng không thể!",
    "🎯 Mục tiêu rõ ràng + hành động quyết tâm = thành công!",
    "🌱 Hôm nay gieo mầm tốt để ngày mai gặt hái thành quả!",
    "🏋️ Hãy rèn luyện cả thể chất lẫn tinh thần mỗi ngày!",
    "🌅 Bình minh mỗi ngày nhắc nhở chúng ta về cơ hội mới!",
    "🎵 Cuộc sống như bản nhạc — hãy chơi hết mình!",
    "🍃 Hít thở không khí trong lành và cảm nhận vẻ đẹp cuộc sống!",
    "🌍 Hãy làm cho thế giới tốt đẹp hơn bắt đầu từ hôm nay!",
    "💡 Ý tưởng lớn bắt đầu từ những suy nghĩ nhỏ vào buổi sáng!",
    "🎊 Chào ngày mới! Mọi chuyện sẽ ổn thôi!",
    "🌟 Hãy tỏa sáng hôm nay và mỗi ngày!",
    "🧩 Mỗi ngày là một mảnh ghép trong bức tranh cuộc đời bạn!",
    "🚂 Đừng dừng lại — hãy tiếp tục tiến về phía trước!",
    "🎈 Hãy nhẹ nhàng và vui vẻ như những quả bóng bay!",
    "🌊 Hãy bình tĩnh như mặt biển vào buổi sáng sớm!",
    "🦋 Hôm nay bạn sẽ chứng kiến sự thay đổi tích cực trong mình!",
    "🌿 Sống chậm lại một chút để cảm nhận những điều tuyệt vời xung quanh!",
    "💎 Bạn là viên kim cương — tỏa sáng dưới áp lực!",
    "🏆 Thành công bắt đầu từ quyết tâm vào buổi sáng!",
    "🌸 Hôm nay hãy yêu thương bản thân và mọi người nhiều hơn!",
    "🎯 Hãy làm một điều nhỏ tiến đến ước mơ lớn hôm nay!",
    "🌞 Nắng mới mỗi ngày — hãy đón nhận với trái tim mở!",
    "🍀 Vận may đang mỉm cười với bạn hôm nay!",
    "🚀 Không gian không là giới hạn — hãy bay cao!",
    "💌 Gửi nụ cười đến mọi người bạn gặp hôm nay!",
    "🎶 Hãy để giai điệu cuộc sống dẫn lối bạn!",
    "🌺 Hôm nay hãy nở rộ như những bông hoa xuân!",
    "🦁 Hãy dũng cảm đối mặt với những thách thức hôm nay!",
    "🌙 Đêm tối đã qua, ngày mới tươi sáng đã đến!",
    "🎁 Chúc bạn nhận được nhiều niềm vui bất ngờ hôm nay!",
    "🏄 Hãy lướt sóng cuộc đời với nụ cười!",
    "🔮 Tương lai tươi sáng bắt đầu từ những hành động hôm nay!",
    "💫 Hãy tin vào hành trình của mình — mọi thứ có lý do!",
    "🌍 Một ngày mới, một cơ hội mới để trở nên tốt hơn!",
    "🎨 Hãy vẽ nên ngày hôm nay bằng những màu sắc tươi vui!",
    "🧡 Tình yêu thương là năng lượng tốt nhất để bắt đầu ngày mới!",
    "🌻 Hướng mặt về phía ánh sáng như hoa hướng dương!",
    "💡 Một ý tưởng hay có thể thay đổi cả ngày của bạn!",
    "🏔️ Mỗi buổi sáng là một đỉnh núi mới cần chinh phục!",
    "🎠 Hãy vui sống từng khoảnh khắc trong ngày hôm nay!",
    "🌈 Cuộc sống đầy màu sắc — hãy trân trọng từng sắc màu!",
    "🍎 Sức khỏe là vàng — hãy chăm sóc bản thân hôm nay!",
    "🌅 Mỗi bình minh là lời nhắc nhở: bạn vẫn còn có cơ hội!",
    "⚡ Hôm nay sẽ là ngày tuyệt vời nhất trong tuần này!",
    "🎉 Chúc mừng bạn đã thức dậy — ngày mới đang chờ bạn!",
    "🌟 Hãy là ngôi sao sáng trong ngày hôm nay!",
    "🌱 Hãy lớn lên và phát triển mỗi ngày!",
]

night_messages = [
    "🌙 Chúc mọi người ngủ ngon và có những giấc mơ đẹp!",
    "💤 Nghỉ ngơi thật tốt sau một ngày dài nhé!",
    "⭐ Đêm nay bầu trời đầy sao — chúc bạn giấc ngủ bình yên!",
    "🌛 Mặt trăng đang canh giữ cho bạn ngủ ngon nhé!",
    "😴 Hãy thả lỏng cơ thể và để giấc ngủ đến tự nhiên!",
    "🌸 Kết thúc ngày với nụ cười — bạn đã làm rất tốt hôm nay!",
    "💫 Ngủ ngon nhé! Ngày mai lại là một ngày mới tươi sáng!",
    "🛏️ Đã đến giờ nghỉ ngơi rồi — hãy để cơ thể hồi phục!",
    "🌿 Hít thở sâu, thư giãn và chìm vào giấc ngủ nhẹ nhàng!",
    "🍵 Uống một ly trà ấm và thư giãn cuối ngày nhé!",
    "🌙 Good night! Cảm ơn vì đã cố gắng hôm nay!",
    "💎 Bạn đã làm rất tốt hôm nay — xứng đáng được nghỉ ngơi!",
    "🌟 Hãy để những lo lắng qua đi và ngủ thật ngon!",
    "🎵 Giai điệu đêm khuya ru bạn vào giấc ngủ êm đềm!",
    "🌺 Chúc đêm nay bình yên và giấc ngủ sâu!",
    "🦋 Ngủ ngon nhé! Ngày mai bạn sẽ bay cao hơn!",
    "🏆 Bạn đã vượt qua một ngày nữa — tuyệt vời lắm!",
    "🌊 Hãy để sóng biển đêm ru bạn vào giấc ngủ!",
    "💌 Gửi ngàn yêu thương trước khi đi ngủ!",
    "🌙 Đêm đã xuống, hãy buông bỏ mọi lo âu và ngủ ngon!",
    "🎁 Giấc ngủ ngon là món quà tốt nhất cho cơ thể bạn!",
    "🌻 Hãy cảm ơn ngày hôm nay và mong chờ ngày mai!",
    "🍀 Chúc bạn có những giấc mơ đẹp và ngủ ngon!",
    "🌈 Sau một ngày đầy màu sắc, giờ là lúc nghỉ ngơi!",
    "💡 Tắt điện thoại sớm và ngủ sớm để có sức khỏe tốt!",
    "🧘 Thiền định vài phút trước khi ngủ để tâm trí bình an!",
    "🌿 Cây cối cũng ngủ vào ban đêm — hãy nghỉ ngơi như thiên nhiên!",
    "🎶 Nghe một bản nhạc nhẹ nhàng trước khi ngủ nhé!",
    "🌛 Trăng lên rồi — đã đến lúc nghỉ ngơi!",
    "💤 Không cần lo lắng — mọi việc sẽ ổn vào ngày mai!",
    "🛡️ Bạn đã làm hết sức hôm nay — hãy tự hào về bản thân!",
    "🌙 Đêm nay hãy ngủ sớm để có năng lượng cho ngày mai!",
    "🎠 Cuộc sống đẹp hơn sau một giấc ngủ ngon!",
    "🦁 Dũng sĩ cũng cần nghỉ ngơi — ngủ ngon bạn nhé!",
    "🌺 Hãy để đêm nay mang lại sự bình yên cho tâm hồn bạn!",
    "⭐ Nhìn lên bầu trời đêm và đếm những điều tốt đẹp hôm nay!",
    "🌍 Nửa bên kia trái đất đang thức, còn bạn hãy ngủ nghỉ!",
    "🎯 Ngủ đủ giấc để ngày mai bạn đạt được mục tiêu!",
    "💪 Cơ thể cần ngủ để phục hồi — hãy cho nó nghỉ ngơi!",
    "🌅 Ngủ ngon để sáng mai đón bình minh với năng lượng mới!",
    "🍎 Ngủ ngon như táo chín — ngọt ngào và bình an!",
    "🎊 Kết thúc ngày với lòng biết ơn — bạn thật may mắn!",
    "🌸 Chúc giấc ngủ nhẹ nhàng như cánh hoa bay!",
    "💡 Tắt hết lo lắng — bật lên giấc ngủ ngon lành!",
    "🚀 Nạp năng lượng qua giấc ngủ để ngày mai chinh phục thế giới!",
    "🌊 Hãy để sóng đêm mang đi mọi mệt mỏi của bạn!",
    "🦋 Biến thành bướm xinh đẹp sau một đêm nghỉ ngơi!",
    "🏔️ Leo lên đỉnh cao nhờ ngủ đủ giấc mỗi đêm!",
    "🎨 Ngủ để não bộ sáng tạo hơn vào ngày mai!",
    "💎 Quý như kim cương, giấc ngủ là tài sản quý nhất của bạn!",
    "🌙 Đêm nay trời trong — ngủ ngon nhé mọi người!",
    "🧡 Gửi yêu thương đến tất cả trước khi chìm vào giấc ngủ!",
    "🌻 Khép lại một ngày đẹp — mong chờ ngày mai tươi sáng hơn!",
    "🎵 Sweet dreams mọi người — ngủ ngon nhé!",
    "🌱 Giống như cây cần đêm để lớn, bạn cần ngủ để phát triển!",
    "🏄 Đã lướt sóng cả ngày rồi — giờ hãy nghỉ ngơi nhé!",
    "🔮 Ngủ ngon để những điều kỳ diệu đến trong giấc mơ!",
    "🌈 Màu cầu vồng sẽ sáng hơn sau đêm nghỉ ngơi!",
    "🍓 Chúc giấc ngủ ngọt như quả dâu tây chín!",
    "🎤 Cất giọng ca tạm biệt ngày và chào đón đêm bình yên!",
    "🌿 Thiên nhiên đang nghỉ ngơi — hãy hòa mình vào nhịp đó!",
    "💫 Những vì sao đang canh giữ giấc ngủ của bạn!",
    "🎈 Thả bóng bay lo lắng và ngủ thật ngon nhé!",
    "🌙 Đêm bình yên gửi đến tất cả mọi người!",
    "🏆 Người chiến thắng biết cách nghỉ ngơi đúng lúc!",
    "💌 Tin nhắn cuối ngày: Bạn thật tuyệt vời hôm nay!",
    "🌊 Hãy để dòng chảy của giấc ngủ mang bạn đến bình yên!",
    "🎁 Tặng bản thân giấc ngủ ngon xứng đáng nhất!",
    "🌺 Hoa khép lại vào ban đêm để nở đẹp hơn vào ban ngày!",
    "⚡ Sạc pin cơ thể qua giấc ngủ để ngày mai bùng cháy!",
    "🦅 Đại bàng cũng nghỉ cánh vào ban đêm — ngủ ngon nhé!",
    "🌛 Mặt trăng tròn đêm nay — chúc bạn giấc ngủ viên mãn!",
    "🎶 Đêm thanh vắng, tiếng nhạc ru, ngủ ngon nhé!",
    "🍵 Uống trà hoa cúc và thả lỏng cơ thể trước khi ngủ!",
    "🌍 Cả thế giới đang ngủ — hãy cùng nghỉ ngơi thôi!",
    "💡 Ý tưởng sáng tạo nhất thường đến sau giấc ngủ ngon!",
    "🧘 Thả lỏng từng cơ bắp và chìm vào giấc ngủ sâu!",
    "🌸 Chúc đêm nay đầy ắp những giấc mơ đẹp đẽ!",
    "🎠 Vòng quay ngày đã dừng lại — đến lúc nghỉ ngơi rồi!",
    "🌿 Hơi thở nhẹ nhàng, tâm trí thư thái — ngủ ngon nhé!",
    "🦋 Bay vào thế giới của những giấc mơ nhé!",
    "💎 Chúc bạn đêm nay bình yên và sang trọng như kim cương!",
    "🌙 Đêm đẹp như tranh — chúc bạn ngủ ngon!",
    "🚀 Tạm biệt ngày hôm nay — đến gặp lại vào sáng mai nhé!",
    "🍀 May mắn sẽ đến cùng giấc ngủ ngon — chúc bạn ngủ tốt!",
    "🌺 Kết thúc hoàn hảo cho một ngày tuyệt vời — ngủ ngon!",
    "🎯 Ngủ đủ giấc để bắn trúng mục tiêu ngày mai!",
    "💪 Cơ thể khỏe mạnh nhờ giấc ngủ đủ giờ mỗi đêm!",
    "🌅 Ngủ ngon để sáng mai chào đón bình minh tươi đẹp!",
    "⭐ Chúc bạn đêm nay đầy ắp những điều bình yên!",
    "🎊 Cảm ơn hôm nay! Chào đón ngày mai! Ngủ ngon nhé!",
    "🌟 Kết thúc ngày bằng lòng biết ơn và ngủ thật ngon!",
    "🌛 Ánh trăng dịu nhẹ ru bạn vào giấc ngủ bình an!",
    "🏄 Đã lướt qua một ngày đẹp — giờ thả trôi vào giấc ngủ!",
    "🎨 Ngủ ngon để vẽ tiếp bức tranh cuộc đời ngày mai!",
    "💫 Chúc bạn những giấc mơ đẹp nhất đêm nay!",
    "🌙 Good night! Cảm ơn vì đã là một phần của ngày hôm nay!",
    "🌻 Ngủ ngon như hoa hướng dương sau một ngày đón nắng!",
    "🍎 Một quả táo mỗi ngày, một giấc ngủ ngon mỗi đêm!",
    "🌈 Sau đêm tối luôn có bình minh — ngủ ngon và tin tưởng!",
]

HOLIDAYS = [
    (1, 1,   "🎆 Tết Dương lịch"),
    (3, 2,   "🔴 Ngày thành lập Đảng CSVN"),
    (8, 3,   "🌹 Ngày Quốc tế Phụ nữ"),
    (26, 3,  "🟡 Ngày thành lập Đoàn TNCS HCM"),
    (30, 4,  "🕊️ Ngày Giải phóng miền Nam"),
    (1, 5,   "✊ Ngày Quốc tế Lao động"),
    (19, 5,  "🌸 Ngày sinh Chủ tịch Hồ Chí Minh"),
    (1, 6,   "🧒 Ngày Quốc tế Thiếu nhi"),
    (27, 7,  "🎖️ Ngày Thương binh Liệt sĩ"),
    (2, 9,   "🇻🇳 Quốc khánh Việt Nam"),
    (20, 10, "🌺 Ngày Phụ nữ Việt Nam"),
    (20, 11, "📐 Ngày Nhà giáo Việt Nam"),
    (22, 12, "⭐ Ngày thành lập Quân đội nhân dân VN"),
    (25, 12, "🎄 Giáng sinh"),
]

daily_facts = [
    "🤓 **Fact:** Mật ong không bao giờ hỏng — người ta tìm thấy mật ong 3000 năm tuổi trong mộ Ai Cập vẫn còn ăn được!",
    "😄 **Joke:** Tại sao lập trình viên không thích ra ngoài? Vì ngoài trời không có WiFi! 😂",
    "🤓 **Fact:** Bạch tuộc có 3 trái tim và máu màu xanh!",
    "😄 **Joke:** Hỏi: Con gì có 4 chân buổi sáng, 2 chân buổi trưa, 3 chân buổi tối? Đáp: Con người! (câu đố của Sphinx đó 😏)",
    "🤓 **Fact:** Cá heo ngủ với một nửa não thức, để không quên thở!",
    "😄 **Joke:** Mẹ hỏi: 'Con học bài chưa?' Con đáp: 'Con đang học ạ.' Mẹ: 'Sao tay cầm điện thoại?' Con: 'Con học... cách buông điện thoại!' 😅",
    "🤓 **Fact:** Một ngày trên sao Kim dài hơn một năm trên sao Kim!",
    "😄 **Joke:** Tại sao con số 6 sợ con số 7? Vì 7 ăn 9 (seven ate nine)! 🍽️",
    "🤓 **Fact:** Chuối là quả mọc ngược — chúng mọc hướng lên trên, không phải xuống!",
    "😄 **Joke:** Bác sĩ hỏi: 'Anh bị đau ở đâu?' Bệnh nhân: 'Ở ví bác sĩ ơi!' 💸",
    "🤓 **Fact:** Sét đánh trái đất khoảng 100 lần mỗi giây!",
    "😄 **Joke:** Học sinh hỏi thầy: 'Thưa thầy, tại sao biển lại mặn?' Thầy: 'Vì cá hay khóc!' 🐟😭",
    "🤓 **Fact:** Người bình thường đi bộ khoảng 5 vòng trái đất trong suốt cuộc đời!",
    "😄 **Joke:** Anh chàng nhắn tin: 'Em ơi anh nhớ em như điên!' Cô gái trả lời: 'Anh là điên!' 😂",
    "🤓 **Fact:** Voi là loài động vật duy nhất không thể nhảy!",
    "😄 **Joke:** Hỏi: Cái gì luôn đến nhưng không bao giờ tới? Đáp: Ngày mai! ⏰",
    "🤓 **Fact:** Nước nóng đóng băng nhanh hơn nước lạnh trong một số điều kiện nhất định — gọi là hiệu ứng Mpemba!",
    "😄 **Joke:** Con nhện hỏi con muỗi: 'Mày có ghét nhện không?' Muỗi: 'Không, tao yêu nhện — mày cứu tao khỏi bị người đập!' 🕷️",
    "🤓 **Fact:** Ngón tay cái của bạn dài bằng mũi của bạn (hãy thử đi, đừng ngại!)!",
    "😄 **Joke:** Tại sao không ai chơi bài với con mèo rừng? Vì nó luôn có con tẩy (cheetah = cheater)! 🃏",
    "🤓 **Fact:** Hươu cao cổ và người có cùng số đốt sống cổ — đều là 7 đốt!",
    "😄 **Joke:** Học sinh: 'Thầy ơi em không hiểu bài.' Thầy: 'Hỏi lại đi.' Học sinh: 'Thầy ơi thầy ơi thầy ơi!' Thầy: '...' 😤",
    "🤓 **Fact:** Sô-cô-la có thể gây độc cho chó và mèo nhưng lại tốt cho con người (nếu ăn vừa phải)!",
    "😄 **Joke:** Hỏi: Cái gì không bao giờ hỏi câu hỏi nhưng luôn cần được trả lời? Đáp: Cái chuông cửa! 🔔",
    "🤓 **Fact:** Oxford là trường đại học lâu đời hơn cả đế chế Aztec của Mexico!",
    "😄 **Joke:** Vợ: 'Anh yêu em hay yêu tiền?' Chồng: 'Anh yêu em! Nhưng tiền thứ hai...' 💕💰",
    "🤓 **Fact:** Cá mập là loài cá cổ hơn cả cây — cá mập xuất hiện trước khi cây có trên Trái Đất!",
    "😄 **Joke:** Sao hôm nay trời nắng đẹp vậy? Vì mây ngại gặp bạn! ☀️",
    "🤓 **Fact:** Honey badger (lửng mật) được Guinness ghi nhận là loài động vật dũng cảm nhất thế giới!",
    "😄 **Joke:** Học bài 1 tiếng = biết 10%. Ngủ 1 tiếng = nạp 100%. Tỉ lệ đầu tư tốt nhất! 😴📚",
    "🤓 **Fact:** Bạn không thể tự hắt hơi khi đang ngủ!",
    "😄 **Joke:** Tại sao cây bút chì thông minh hơn cây bút bi? Vì nó có điểm (point) hơn! ✏️",
    "🤓 **Fact:** Mắt của đà điểu to hơn não của nó!",
    "😄 **Joke:** Hỏi: Tại sao bò không dùng điện thoại? Đáp: Vì đã có bướm (bướm = butterfly, còn bò = cow)! 🐄🦋",
    "🤓 **Fact:** Trung bình mỗi người ăn khoảng 8 con nhện trong lúc ngủ mỗi năm... (thực ra đây là tin giả nhưng vui!) 🕷️😂",
    "😄 **Joke:** Con ếch gặp con rắn: 'Mày có ăn tao không?' Rắn: 'Không.' Ếch: 'Ủa, mày ăn chay à?' Rắn: 'Không, tao đang no!' 🐸🐍",
    "🤓 **Fact:** Nếu bạn đào một cái hố xuyên tâm Trái Đất, bạn sẽ không ra phía bên kia mà sẽ bị kéo lui lại giữa!",
    "😄 **Joke:** Bạn biết tại sao ngư dân buồn không? Vì nghề của họ... có nhiều thăng trầm (lên xuống như sóng)! 🎣",
    "🤓 **Fact:** Nước sôi có thể đóng băng nhanh hơn nước lạnh trong điều kiện nhất định — khoa học vẫn chưa giải thích hoàn toàn!",
    "😄 **Joke:** Tại sao ma không bao giờ nói dối? Vì chúng luôn... trong suốt (transparent)! 👻",
    "🤓 **Fact:** Sóc thường quên mất nơi chúng chôn hạt — vô tình trở thành 'người' trồng cây nhiều nhất!",
    "😄 **Joke:** Học sinh hỏi: 'Thầy ơi điểm 0 nghĩa là gì?' Thầy: 'Nghĩa là con số không có ý nghĩa — giống như bài làm của em!' 😅",
    "🤓 **Fact:** Mặt trăng đang dần xa Trái Đất khoảng 3.8 cm mỗi năm!",
    "😄 **Joke:** Hỏi: Cái gì có đầu nhưng không có não? Đáp: Cây đinh! 🔨",
    "🤓 **Fact:** Người có thể sống không có thức ăn 3 tuần nhưng không có nước chỉ 3 ngày!",
    "😄 **Joke:** Vì sao con voi mặc quần đỏ? Để trốn trong rừng táo mà không ai thấy! Bạn đã thấy voi trong rừng táo chưa? Đó, hiệu quả lắm! 🐘🍎",
    "🤓 **Fact:** Tiếng sấm là âm thanh của không khí giãn nở cực nhanh do nhiệt của tia sét!",
    "😄 **Joke:** Bố hỏi: 'Con học bài chưa?' Con: 'Rồi bố.' Bố: 'Sao TV vẫn bật?' Con: 'Con học bằng mắt nên cần tắt tai ạ!' 📺",
    "🤓 **Fact:** Nếu bạn xếp tất cả DNA trong cơ thể thẳng ra, nó dài đủ đi từ Trái Đất đến Diêm Vương Tinh và quay về!",
    "😄 **Joke:** Hỏi: Tại sao chim không dùng Facebook? Đáp: Vì chúng đã có Twitter (tweet = tiếng chim hót)! 🐦",
    "🤓 **Fact:** Cà chua được phân loại là quả, không phải rau — nhưng Tòa án Tối cao Mỹ năm 1893 tuyên bố nó là rau để đánh thuế!",
]

def get_upcoming_holiday():
    today = datetime.now()
    current_day = today.day
    current_month = today.month
    current_year = today.year

    closest = None
    min_days = 366

    for day, month, name in HOLIDAYS:
        try:
            hdate = datetime(current_year, month, day)
        except ValueError: continue
        if hdate < today.replace(hour=0, minute=0, second=0, microsecond=0):
            hdate = datetime(current_year + 1, month, day)
        delta = (hdate - today.replace(hour=0, minute=0, second=0, microsecond=0)).days
        if delta < min_days:
            min_days = delta
            closest = (day, month, name, delta)

    if closest is None: return ""
    day, month, name, delta = closest
    if delta == 0: return f"🎉 **Hôm nay là {name}!** Chúc mừng ngày lễ!"
    elif delta == 1: return f"📅 **Ngày mai là {name}!** Chuẩn bị đón lễ nhé!"
    else: return f"📅 Còn **{delta} ngày** nữa là đến **{name}** ({day}/{month})."

# Cấu hình file lưu dữ liệu
XP_FILE = "xp_data.json"
COMMANDS_FILE = "custom_commands.json"
AUTO_RESPONSES_FILE = "auto_responses.json"

XP_COOLDOWN = {}

LEVEL_ROLES = [
    (0,       "🌱 Người Mới"), (200,     "🌿 Người Quen"), (500,     "🌳 Thành Viên"),
    (1000,    "💬 Hay Nói Chuyện"), (2000,    "⭐ Hoạt Động"), (3500,    "🔵 Tích Cực"),
    (5500,    "🟢 Cựu Thành Viên"), (8000,    "🔥 Nhiệt Huyết"), (11000,   "💪 Chiến Binh"),
    (15000,   "⚡ Siêu Năng Động"), (20000,   "🎯 Chuyên Gia"), (27000,   "🌟 Ngôi Sao"),
    (36000,   "🏅 Hào Quang"), (47000,   "🥇 Vô Địch"), (60000,   "💎 Kim Cương"),
    (76000,   "🔮 Huyền Bí"), (95000,   "👑 Hoàng Gia"), (120000,  "🌈 Huyền Thoại"),
    (150000,  "🦋 Siêu Huyền Thoại"), (200000,  "🏆 Bất Tử"),
]

def get_level_role(xp):
    current_role = LEVEL_ROLES[0][1]
    for threshold, role_name in LEVEL_ROLES:
        if xp >= threshold: current_role = role_name
        else: break
    return current_role

def load_json(path):
    if not os.path.exists(path): return {}
    try:
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=2, ensure_ascii=False)

async def give_xp(message):
    import time
    user_id = str(message.author.id)
    now = time.time()
    if user_id in XP_COOLDOWN and now - XP_COOLDOWN[user_id] < 60: return
    XP_COOLDOWN[user_id] = now
    xp_data = load_json(XP_FILE)
    if user_id not in xp_data: xp_data[user_id] = {"xp": 0, "role": LEVEL_ROLES[0][1]}
    old_role = get_level_role(xp_data[user_id]["xp"])
    xp_data[user_id]["xp"] += min(len(message.content), 200)
    new_role = get_level_role(xp_data[user_id]["xp"])
    save_json(XP_FILE, xp_data)
    if new_role != old_role and message.guild:
        await message.channel.send(f"🎉 {message.author.mention} đã lên cấp: **{new_role}**!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_morning_day = None
last_night_day = None

@bot.event
async def on_ready():
    print(f"Bot {bot.user} đã sẵn sàng!")
    auto_message.start()

@tasks.loop(minutes=1)
async def auto_message():
    global last_morning_day, last_night_day
    now = datetime.now()
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
    except: return
    if now.hour == 7 and now.minute == 0 and last_morning_day != now.day:
        await channel.send(f"☀️ {random.choice(morning_messages)}\nHôm nay là {now.day}/{now.month}/{now.year}")
        last_morning_day = now.day
    if now.hour == 23 and now.minute == 0 and last_night_day != now.day:
        await channel.send(f"🌙 {random.choice(night_messages)}")
        last_night_day = now.day

@bot.event
async def on_message(message):
    if message.author.bot: return
    content_lower = message.content.lower()
    auto_responses = load_json(AUTO_RESPONSES_FILE)
    for trigger, response in auto_responses.items():
        if trigger.lower() in content_lower:
            await message.channel.send(response)
            break
    if message.content.startswith(bot.command_prefix):
        cmd_name = message.content[len(bot.command_prefix):].split()[0].lower()
        custom_commands = load_json(COMMANDS_FILE)
        if cmd_name in custom_commands:
            await message.channel.send(custom_commands[cmd_name])
            return
    await give_xp(message)
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_guild=True)
async def addcmd(ctx, name: str, *, response: str):
    data = load_json(COMMANDS_FILE)
    data[name.lower()] = response
    save_json(COMMANDS_FILE, data)
    await ctx.send(f"Đã thêm lệnh `!{name}`")

# Kích hoạt web server trước khi chạy bot
keep_alive() 
bot.run(TOKEN)
