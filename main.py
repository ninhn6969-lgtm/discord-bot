import os
import json
import random
import requests
import discord
from flask import Flask
from threading import Thread
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask_server)
    t.start()
# --- CẤU HÌNH BIẾN ---
load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
WEATHER_API = "16dd80ccb3b2e13098744cad826085b2"
CHANNEL_ID = 1437653177846599852

cities = [
    ("Hà Nội", "Hanoi"), ("Hạ Long", "Ha Long"),
    ("Thanh Hóa", "Thanh Hoa"), ("TP.HCM", "Ho Chi Minh City")
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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
    "🌊 Để sóng đêm mang đi mọi mệt mỏi của bạn!",
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
        hdate = datetime(current_year, month, day)
        if hdate < today.replace(hour=0, minute=0, second=0, microsecond=0):
            hdate = datetime(current_year + 1, month, day)
        delta = (hdate - today.replace(hour=0, minute=0, second=0, microsecond=0)).days
        if delta < min_days:
            min_days = delta
            closest = (day, month, name, delta)

    if closest is None:
        return ""
    day, month, name, delta = closest
    if delta == 0:
        return f"🎉 **Hôm nay là {name}!** Chúc mừng ngày lễ!"
    elif delta == 1:
        return f"📅 **Ngày mai là {name}!** Chuẩn bị đón lễ nhé!"
    elif delta <= 7:
        return f"📅 Còn **{delta} ngày** nữa là đến **{name}** ({day}/{month})!"
    elif delta <= 30:
        return f"📅 Còn **{delta} ngày** nữa là đến **{name}** ({day}/{month})."
    else:
        return f"📅 Ngày lễ gần nhất: **{name}** ({day}/{month}) — còn {delta} ngày."


XP_FILE = "bot/xp_data.json"
XP_COOLDOWN = {}

LEVEL_ROLES = [
    (0,       "🌱 Người Mới"),
    (200,     "🌿 Người Quen"),
    (500,     "🌳 Thành Viên"),
    (1000,    "💬 Hay Nói Chuyện"),
    (2000,    "⭐ Hoạt Động"),
    (3500,    "🔵 Tích Cực"),
    (5500,    "🟢 Cựu Thành Viên"),
    (8000,    "🔥 Nhiệt Huyết"),
    (11000,   "💪 Chiến Binh"),
    (15000,   "⚡ Siêu Năng Động"),
    (20000,   "🎯 Chuyên Gia"),
    (27000,   "🌟 Ngôi Sao"),
    (36000,   "🏅 Hào Quang"),
    (47000,   "🥇 Vô Địch"),
    (60000,   "💎 Kim Cương"),
    (76000,   "🔮 Huyền Bí"),
    (95000,   "👑 Hoàng Gia"),
    (120000,  "🌈 Huyền Thoại"),
    (150000,  "🦋 Siêu Huyền Thoại"),
    (200000,  "🏆 Bất Tử"),
]


def get_level_role(xp):
    current_role = LEVEL_ROLES[0][1]
    for threshold, role_name in LEVEL_ROLES:
        if xp >= threshold:
            current_role = role_name
        else:
            break
    return current_role


def get_next_level(xp):
    for threshold, role_name in LEVEL_ROLES:
        if xp < threshold:
            return threshold, role_name
    return None, None


def load_xp():
    if not os.path.exists(XP_FILE):
        return {}
    with open(XP_FILE, "r") as f:
        return json.load(f)


def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=2)


async def give_xp(message):
    import time
    user_id = str(message.author.id)
    now = time.time()

    if user_id in XP_COOLDOWN and now - XP_COOLDOWN[user_id] < 60:
        return

    XP_COOLDOWN[user_id] = now

    xp_data = load_xp()
    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "role": LEVEL_ROLES[0][1]}

    old_role = get_level_role(xp_data[user_id]["xp"])
    char_xp = min(len(message.content), 200)
    xp_data[user_id]["xp"] += char_xp
    new_xp = xp_data[user_id]["xp"]
    new_role = get_level_role(new_xp)

    save_xp(xp_data)

    if new_role != old_role and message.guild:
        member = message.guild.get_member(message.author.id)
        if member:
            for _, role_name in LEVEL_ROLES:
                existing = discord.utils.get(message.guild.roles, name=role_name)
                if existing and existing in member.roles:
                    try:
                        await member.remove_roles(existing)
                    except Exception:
                        pass

            new_discord_role = discord.utils.get(message.guild.roles, name=new_role)
            if not new_discord_role:
                try:
                    new_discord_role = await message.guild.create_role(name=new_role, reason="Level up!")
                except Exception:
                    pass
            if new_discord_role:
                try:
                    await member.add_roles(new_discord_role)
                except Exception:
                    pass

            await message.channel.send(
                f"🎉 Chúc mừng {message.author.mention}! Bạn đã lên cấp mới: **{new_role}**! (XP: {new_xp})"
            )


intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Cần bật "Server Members Intent" trong Discord Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)

COMMANDS_FILE = "bot/custom_commands.json"
AUTO_RESPONSES_FILE = "bot/auto_responses.json"

last_morning_day = None
last_night_day = None

DEDUP_FILE = "bot/dedup.json"
DEDUP_TTL = 60  # giây


def is_duplicate(key):
    import time
    try:
        with open(DEDUP_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
    now = time.time()
    data = {k: v for k, v in data.items() if now - v < DEDUP_TTL}
    if key in data:
        try:
            with open(DEDUP_FILE, "w") as f:
                json.dump(data, f)
        except Exception:
            pass
        return True
    data[key] = now
    try:
        with open(DEDUP_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass
    return False


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


AQI_LABELS = {
    1: "Tốt 🟢",
    2: "Khá 🟡",
    3: "Trung bình 🟠",
    4: "Kém 🔴",
    5: "Rất kém 🟣"
}


def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API}&units=metric&lang=vi"
    )
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        aqi_url = (
            f"http://api.openweathermap.org/data/2.5/air_pollution"
            f"?lat={lat}&lon={lon}&appid={WEATHER_API}"
        )
        aqi_response = requests.get(aqi_url, timeout=10)
        aqi_data = aqi_response.json()
        aqi = aqi_data["list"][0]["main"]["aqi"]
        aqi_label = AQI_LABELS.get(aqi, "Không rõ")

        return f"{temp}°C - {weather} | 💧 Độ ẩm: {humidity}% | 🌬️ KK: {aqi_label}", temp
    except Exception:
        return "Không lấy được dữ liệu", None


def water_tip_from_temps(temps):
    """Tính gợi ý uống nước từ danh sách nhiệt độ đã lấy sẵn — không gọi API thêm."""
    valid = [t for t in temps if t is not None]
    avg_temp = sum(valid) / len(valid) if valid else None

    if avg_temp is None:
        liters, note = 2.5, ""
    elif avg_temp >= 37:
        liters, note = 3.5, "🥵 Trời rất nóng, cần uống nhiều hơn bình thường!"
    elif avg_temp >= 33:
        liters, note = 3.0, "☀️ Trời nóng, nhớ uống đủ nước để tránh mất nước nhé!"
    elif avg_temp >= 28:
        liters, note = 2.5, "🌤️ Thời tiết ấm, duy trì uống nước đều đặn nhé!"
    elif avg_temp >= 22:
        liters, note = 2.0, "🌿 Thời tiết dễ chịu, uống nước đều theo giờ nhé!"
    else:
        liters, note = 1.8, "🌧️ Trời mát, nhưng vẫn đừng quên uống nước nhé!"

    temp_str = f" (nhiệt độ TB: {avg_temp:.1f}°C)" if avg_temp is not None else ""
    return (
        f"💧 **Hôm nay nên uống khoảng {liters} lít nước**{temp_str}\n"
        f"   {note}\n"
        f"   *(Chia đều ~{round(liters/8, 1)} lít mỗi 2 tiếng — 8 lần/ngày)*"
    )


def get_forecast_at(city, target_hour):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={WEATHER_API}&units=metric&lang=vi&cnt=8"
    )
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        forecasts = data["list"]
        today = datetime.now().strftime("%Y-%m-%d")

        best = None
        for item in forecasts:
            dt_txt = item["dt_txt"]
            if not dt_txt.startswith(today):
                continue
            hour = int(dt_txt[11:13])
            if best is None or abs(hour - target_hour) < abs(int(best["dt_txt"][11:13]) - target_hour):
                best = item

        if best is None:
            return "Không có dữ liệu"

        temp = best["main"]["temp"]
        humidity = best["main"]["humidity"]
        desc = best["weather"][0]["description"]
        return f"{temp}°C - {desc} | 💧 {humidity}%"
    except Exception:
        return "Không lấy được dữ liệu"


# --- SETUP BOT ---
# --- 3. SETUP BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API}&units=metric&lang=vi"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"{temp}°C, {desc}"
    return "Không lấy được thông tin thời tiết."

@tasks.loop(minutes=1)
async def check_time():
    now_vn = datetime.utcnow() + timedelta(hours=7)
    current_time = now_vn.strftime("%H:%M")
    print(f"Log: Giờ VN hiện tại là {current_time}")

    channel = bot.get_channel(CHANNEL_ID)
    if not channel: return

    if current_time == "07:00":
        msg = random.choice(morning_messages)
        await channel.send(f"☀️ **Chào buổi sáng!**\n{msg}")
    if current_time == "23:00":
        await channel.send("🌙 Đã đến giờ đi ngủ rồi, chúc cả nhà ngủ ngon!")

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} đã kết nối thành công!')
    if not check_time.is_running():
        check_time.start()
# --- HÀM KIỂM TRA GIỜ VIỆT NAM ---
@tasks.loop(minutes=1)
async def check_time():
    now_vn = datetime.utcnow() + timedelta(hours=7)
    current_time = now_vn.strftime("%H:%M")
    print(f"Log: Giờ VN hiện tại là {current_time}")

    channel = bot.get_channel(CHANNEL_ID)
    if not channel: return

    # Chào buổi sáng 7:00 AM VN
    if current_time == "07:00":
            await channel.send(
                f"☀️ Good Morning mọi người!\n\n"
                f"📅 Hôm nay là ngày {day}/{month}/{year}\n\n"
                f"**🌡️ Thời tiết buổi sáng:**\n{weather_text}\n"
                f"**💧 Lượng nước cần uống hôm nay:**\n{water_tip}\n\n"
                f"**🍱 Dự báo buổi trưa (11h-13h):**\n{noon_text}\n"
                f"**🌇 Dự báo buổi chiều (17h-19h):**\n{afternoon_text}\n"
                f"{holiday_text}\n\n"
                f"**🎲 Fact/Joke trong ngày:**\n{fact_text}\n\n"
                f"{random_message}"
            )
            last_morning_day = day

    # Chúc ngủ ngon 23:00 PM VN
    if current_time == "23:00":
            await channel.send(
                f"🌙 Good Night mọi người!\n\n"
                f"📅 Hôm nay là ngày {day}/{month}/{year}\n\n"
                f"{weather_text}\n"
                f"{random_message}"
            )
            last_night_day = day

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} đã kết nối thành công!')
    if not check_time.is_running():
        check_time.start()

async def on_member_join(member):
    xp_data = load_xp()
    user_id = str(member.id)
    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "role": LEVEL_ROLES[0][1]}
        save_xp(xp_data)

    first_role_name = LEVEL_ROLES[0][1]
    role = discord.utils.get(member.guild.roles, name=first_role_name)
    if not role:
        try:
            role = await member.guild.create_role(name=first_role_name, reason="Role mặc định cho thành viên mới")
        except Exception:
            return
    try:
        await member.add_roles(role)
    except Exception:
        pass


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    if not message.content.startswith(bot.command_prefix):
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
@bot.command(name="time")
async def time_vn(ctx):
    now_vn = datetime.utcnow() + timedelta(hours=7)
    await ctx.send(f"🕒 Giờ VN hiện tại bot nhận là: {now_vn.strftime('%H:%M:%S')}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Bot đang chạy ổn định.")

@bot.command(name="addcmd")
@commands.has_permissions(manage_guild=True)
async def add_command(ctx, name: str, *, response: str):
    """Thêm lệnh tùy chỉnh. Dùng: !addcmd <tên> <nội dung>"""
    custom_commands = load_json(COMMANDS_FILE)
    custom_commands[name.lower()] = response
    save_json(COMMANDS_FILE, custom_commands)
    await ctx.send(f"Đã thêm lệnh `!{name}`!")


@bot.command(name="removecmd")
@commands.has_permissions(manage_guild=True)
async def remove_command(ctx, name: str):
    """Xóa lệnh tùy chỉnh. Dùng: !removecmd <tên>"""
    custom_commands = load_json(COMMANDS_FILE)
    if name.lower() in custom_commands:
        del custom_commands[name.lower()]
        save_json(COMMANDS_FILE, custom_commands)
        await ctx.send(f"Đã xóa lệnh `!{name}`.")
    else:
        await ctx.send(f"Không tìm thấy lệnh `!{name}`.")


@bot.command(name="listcmds")
async def list_commands(ctx):
    """Xem danh sách lệnh tùy chỉnh."""
    custom_commands = load_json(COMMANDS_FILE)
    if not custom_commands:
        await ctx.send("Chưa có lệnh tùy chỉnh nào.")
        return
    cmds = "\n".join([f"`!{k}` — {v}" for k, v in custom_commands.items()])
    embed = discord.Embed(title="Lệnh tùy chỉnh", description=cmds, color=0x5865F2)
    await ctx.send(embed=embed)


@bot.command(name="addauto")
@commands.has_permissions(manage_guild=True)
async def add_auto(ctx, trigger: str, *, response: str):
    """Thêm auto-response. Dùng: !addauto <trigger> <nội dung>"""
    auto_responses = load_json(AUTO_RESPONSES_FILE)
    auto_responses[trigger.lower()] = response
    save_json(AUTO_RESPONSES_FILE, auto_responses)
    await ctx.send(f"Đã thêm auto-response cho `{trigger}`!")


@bot.command(name="removeauto")
@commands.has_permissions(manage_guild=True)
async def remove_auto(ctx, trigger: str):
    """Xóa auto-response. Dùng: !removeauto <trigger>"""
    auto_responses = load_json(AUTO_RESPONSES_FILE)
    if trigger.lower() in auto_responses:
        del auto_responses[trigger.lower()]
        save_json(AUTO_RESPONSES_FILE, auto_responses)
        await ctx.send(f"Đã xóa auto-response cho `{trigger}`.")
    else:
        await ctx.send(f"Không tìm thấy auto-response cho `{trigger}`.")


@bot.command(name="listauto")
async def list_auto(ctx):
    """Xem danh sách auto-response."""
    auto_responses = load_json(AUTO_RESPONSES_FILE)
    if not auto_responses:
        await ctx.send("Chưa có auto-response nào.")
        return
    items = "\n".join([f"`{k}` → {v}" for k, v in auto_responses.items()])
    embed = discord.Embed(title="Auto-Responses", description=items, color=0x57F287)
    await ctx.send(embed=embed)


@bot.command(name="schedule")
async def schedule(ctx):
    """Xem lịch gửi tin nhắn tự động."""
    now = datetime.now()
    day = now.day

    morning_status = "✅ Đã gửi hôm nay" if last_morning_day == day else "⏳ Chưa gửi hôm nay"
    night_status = "✅ Đã gửi hôm nay" if last_night_day == day else "⏳ Chưa gửi hôm nay"

    embed = discord.Embed(title="📅 Lịch tin nhắn tự động", color=0xFFA500)
    embed.add_field(
        name="☀️ Good Morning",
        value=f"Gửi lúc **07:00** mỗi ngày\nTrạng thái: {morning_status}",
        inline=False
    )
    embed.add_field(
        name="🌙 Good Night",
        value=f"Gửi lúc **23:00** mỗi ngày\nTrạng thái: {night_status}",
        inline=False
    )
    embed.add_field(
        name="🕐 Giờ hiện tại",
        value=f"`{now.strftime('%H:%M:%S')}` ngày {now.strftime('%d/%m/%Y')}",
        inline=False
    )
    await ctx.send(embed=embed)


@bot.command(name="testmsg")
@commands.has_permissions(manage_guild=True)
async def testmsg(ctx, loai: str = "morning"):
    """Gửi thử tin nhắn tự động. Dùng: !testmsg morning | !testmsg night"""
    # Dùng xóa tin lệnh làm khóa nguyên tử — phiên nào xóa được thì chạy,
    # phiên còn lại nhận NotFound và dừng ngay, tránh gửi lặp.
    try:
        await ctx.message.delete()
    except discord.NotFound:
        return  # Phiên bot khác đã xử lý rồi
    except Exception:
        pass  # Không có quyền xóa — vẫn tiếp tục nhưng chấp nhận rủi ro

    now = datetime.now()
    day, month, year = now.day, now.month, now.year

    weather_text = ""
    collected_temps = []
    for city_name, city_api in cities:
        weather, temp = get_weather(city_api)
        weather_text += f"🌤️ {city_name}: {weather}\n"
        collected_temps.append(temp)

    if loai.lower() in ("morning", "sang", "sáng"):
        noon_text = ""
        afternoon_text = ""
        for city_name, city_api in cities:
            noon_text += f"🌞 {city_name}: {get_forecast_at(city_api, 12)}\n"
            afternoon_text += f"🌆 {city_name}: {get_forecast_at(city_api, 18)}\n"

        holiday_text = get_upcoming_holiday()
        fact_text = random.choice(daily_facts)
        water_tip = water_tip_from_temps(collected_temps)

        await ctx.send(
            f"☀️ Good Morning mọi người!\n\n"
            f"📅 Hôm nay là ngày {day}/{month}/{year}\n\n"
            f"**🌡️ Thời tiết buổi sáng:**\n{weather_text}\n"
            f"**💧 Lượng nước cần uống hôm nay:**\n{water_tip}\n\n"
            f"**🍱 Dự báo buổi trưa (11h-13h):**\n{noon_text}\n"
            f"**🌇 Dự báo buổi chiều (17h-19h):**\n{afternoon_text}\n"
            f"{holiday_text}\n\n"
            f"**🎲 Fact/Joke trong ngày:**\n{fact_text}\n\n"
            f"{random.choice(morning_messages)}"
        )

    elif loai.lower() in ("night", "toi", "tối"):
        await ctx.send(
            f"🌙 Good Night mọi người!\n\n"
            f"📅 Hôm nay là ngày {day}/{month}/{year}\n\n"
            f"{weather_text}\n"
            f"{random.choice(night_messages)}"
        )

    else:
        await ctx.send("❌ Dùng: `!testmsg morning` hoặc `!testmsg night`")


@bot.command(name="rank")
async def rank(ctx, member: discord.Member = None):
    """Xem XP và cấp độ. Dùng: !rank hoặc !rank @người"""
    target = member or ctx.author
    xp_data = load_xp()
    user_id = str(target.id)

    if user_id not in xp_data:
        xp_data[user_id] = {"xp": 0, "role": LEVEL_ROLES[0][1]}

    xp = xp_data[user_id]["xp"]
    current_role = get_level_role(xp)
    next_threshold, next_role = get_next_level(xp)

    embed = discord.Embed(title=f"📊 Rank của {target.display_name}", color=0xF1C40F)
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="🏅 Cấp hiện tại", value=current_role, inline=True)
    embed.add_field(name="⚡ XP", value=f"{xp} XP", inline=True)

    if next_threshold:
        prev_threshold = 0
        for t, _ in LEVEL_ROLES:
            if t < next_threshold and t <= xp:
                prev_threshold = t
        span = next_threshold - prev_threshold
        progress = xp - prev_threshold
        bar_fill = int(progress / span * 10) if span > 0 else 10
        bar_fill = max(0, min(10, bar_fill))
        bar = "🟩" * bar_fill + "⬛" * (10 - bar_fill)
        embed.add_field(
            name="📈 Lên cấp tiếp theo",
            value=f"**{next_role}** — còn **{next_threshold - xp} XP** ({progress}/{span})",
            inline=False
        )
        embed.add_field(name="Tiến độ", value=bar, inline=False)
    else:
        embed.add_field(name="📈 Cấp độ", value="Đã đạt cấp tối đa! 👑", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="leaderboard", aliases=["lb", "top"])
async def leaderboard(ctx):
    """Xem bảng xếp hạng XP top 10."""
    xp_data = load_xp()
    if not xp_data:
        await ctx.send("Chưa có ai tích lũy XP cả!")
        return

    sorted_users = sorted(xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]

    embed = discord.Embed(title="🏆 Bảng Xếp Hạng XP", color=0xE67E22)
    medals = ["🥇", "🥈", "🥉"] + ["4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    desc = ""
    for i, (uid, data) in enumerate(sorted_users):
        try:
            user = ctx.guild.get_member(int(uid))
            name = user.display_name if user else f"User {uid[:6]}"
        except Exception:
            name = f"User {uid[:6]}"
        role = get_level_role(data["xp"])
        desc += f"{medals[i]} **{name}** — {data['xp']} XP | {role}\n"

    embed.description = desc
    await ctx.send(embed=embed)


@bot.command(name="resetxp")
@commands.has_permissions(manage_guild=True)
async def reset_xp(ctx, member: discord.Member):
    """Reset XP của một thành viên. Dùng: !resetxp @người"""
    xp_data = load_xp()
    user_id = str(member.id)
    if user_id in xp_data:
        xp_data[user_id]["xp"] = 0
        save_xp(xp_data)
    await ctx.send(f"✅ Đã reset XP của {member.mention}.")


@bot.command(name="setuproles")
@commands.has_permissions(manage_guild=True, manage_roles=True)
async def setup_roles(ctx):
    """Tạo toàn bộ role cấp độ trong server. Dùng: !setuproles"""
    msg = await ctx.send("⏳ Đang tạo các role cấp độ...")
    created = []
    existed = []

    role_colors = [
        0x95a5a6,  # 🌱 Người Mới - xám
        0x2ecc71,  # 🌿 Người Quen - xanh lá nhạt
        0x27ae60,  # 🌳 Thành Viên - xanh lá
        0x1abc9c,  # 💬 Hay Nói Chuyện - ngọc
        0x3498db,  # ⭐ Hoạt Động - xanh dương
        0x2980b9,  # 🔵 Tích Cực - xanh đậm
        0x9b59b6,  # 🟢 Cựu Thành Viên - tím
        0xe67e22,  # 🔥 Nhiệt Huyết - cam
        0xe74c3c,  # 💪 Chiến Binh - đỏ
        0xf39c12,  # ⚡ Siêu Năng Động - vàng
        0xd35400,  # 🎯 Chuyên Gia - cam đậm
        0xf1c40f,  # 🌟 Ngôi Sao - vàng sáng
        0x16a085,  # 🏅 Hào Quang - xanh ngọc đậm
        0xc0392b,  # 🥇 Vô Địch - đỏ đậm
        0x1f8ef1,  # 💎 Kim Cương - xanh kim cương
        0x8e44ad,  # 🔮 Huyền Bí - tím đậm
        0xf6c90e,  # 👑 Hoàng Gia - vàng hoàng gia
        0xe91e63,  # 🌈 Huyền Thoại - hồng
        0xff5722,  # 🦋 Siêu Huyền Thoại - đỏ cam
        0xffd700,  # 🏆 Bất Tử - vàng rực
    ]

    for i, (threshold, role_name) in enumerate(LEVEL_ROLES):
        existing = discord.utils.get(ctx.guild.roles, name=role_name)
        if existing:
            existed.append(role_name)
        else:
            color = discord.Color(role_colors[i]) if i < len(role_colors) else discord.Color.default()
            try:
                await ctx.guild.create_role(
                    name=role_name,
                    color=color,
                    reason=f"Level role — cần {threshold} XP"
                )
                created.append(role_name)
            except Exception as e:
                await ctx.send(f"❌ Lỗi khi tạo role `{role_name}`: {e}")

    lines = []
    if created:
        lines.append(f"✅ **Đã tạo {len(created)} role mới:**")
        for r in created:
            lines.append(f"  • {r}")
    if existed:
        lines.append(f"\n⚠️ **{len(existed)} role đã tồn tại** (bỏ qua):")
        for r in existed:
            lines.append(f"  • {r}")

    await msg.edit(content="\n".join(lines) or "✅ Hoàn thành!")


@bot.command(name="ping")
async def ping(ctx):
    """Kiểm tra độ trễ bot."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Độ trễ: {latency}ms")


@bot.command(name="say")
@commands.has_permissions(manage_guild=True)
async def say(ctx, *, message: str):
    """Bot gửi tin nhắn. Dùng: !say <nội dung>"""
    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name="weather")
async def weather_cmd(ctx, *, city: str = None):
    """Xem thời tiết. Dùng: !weather <thành phố>"""
    if city is None:
        weather_text = ""
        for city_name, city_api in cities:
            w = get_weather(city_api)
            weather_text += f"🌤️ {city_name}: {w}\n"
        embed = discord.Embed(title="Thời tiết hôm nay", description=weather_text, color=0x00BFFF)
        await ctx.send(embed=embed)
    else:
        w = get_weather(city)
        await ctx.send(f"🌤️ **{city}**: {w}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bạn không có quyền dùng lệnh này.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Thiếu tham số. Dùng `!help {ctx.command}` để xem hướng dẫn.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Error: {error}")

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    if not TOKEN:
        print("LỖI: Thiếu Token!")
        exit(1)
    keep_alive()  # Gọi hàm ở Phần 2
    bot.run(TOKEN) # Lệnh này phải là lệnh CUỐI CÙNG
