import osimport timeimport requestsimport youtube_dlfrom pyrogram import filters, Client, enumsfrom youtube_search import YoutubeSearchfrom pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup@Client.on_message(filters.command(['status']))async def online(client, message):	await message.reply(f"Бот онлайн.\n\n\n",	                    disable_web_page_preview=True)@Client.on_message(filters.command(['start']))async def start(client, message):	await message.reply("Поехали!")@Client.on_message(filters.command(['about']))async def about(client, message):	await message.reply(		"🎵️Бот: <i>Youtube to MP3</i>\n🕵️‍♂️ </b>Админ</b> : [ls500pymaster](https://t.me/alexexalex)\n🐍 <b>Язык</b> : <i>Python 3</i>\n",		reply_markup=InlineKeyboardMarkup(			[				[					InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')				]			]		)	)@Client.on_message(filters.command("song"))def song(_, message):	query = "".join(" " + str(i) for i in message.command[1:]).partition("&")	m = message.reply('🔎 Начинаю поиск ...')	ydl_opts = {"format": "bestaudio[ext=m4a]",	            "cachedir": False,	            "nocheckcertificate": True,	            " ignoreerrors": True,	            }	try:		results = []		count = 0		while len(results) == 0 and count < 6:			if count > 0:				time.sleep(1)			results = YoutubeSearch(query[0], max_results=1).to_dict()			count += 1		try:			link = f"https://youtube.com{results[0]['url_suffix']}"			title = results[0]["title"]			thumbnail = results[0]["thumbnails"][0]			duration = results[0]["duration"]			views = results[0]["views"]			thumb_name = f"thumb{id(message)}.jpg"			thumb = requests.get(thumbnail, allow_redirects=True)			open(thumb_name, "wb").write(thumb.content)		except Exception as e:			print(e)			m.edit("Ничего не найдено. Ссылка точно не кривая?")			return	except Exception as e:		m.edit(			"Что-то пошло не так..."		)		print(str(e))		return	m.edit("⏬ Загружаю...")	try:		with youtube_dl.YoutubeDL(ydl_opts) as ydl:			ydl.cache.remove()			info_dict = ydl.extract_info(link, download=False)			audio_file = ydl.prepare_filename(info_dict)			ydl.process_info(info_dict)		result_info = f"🎧 Трек: [{title[:35]}]({link})\n⏳ Время: {duration}\n➡️ Просмотры: {views}\n🤘 Спарсил: {message.from_user.mention()}\n"		secmul, dur, dur_arr = 1, 0, duration.split(":")		for i in range(len(dur_arr) - 1, -1, -1):			dur += int(dur_arr[i]) * secmul			secmul *= 60		parse_mode = enums.ParseMode.HTML		message.reply_audio(audio_file, caption=result_info, parse_mode=parse_mode, quote=False, title=title, duration=dur, thumb=thumb_name)		m.delete()	except Exception as e:		m.edit('Fail! Exception...')		print(e)	try:		os.remove(audio_file)		os.remove(thumb_name)	except Exception as e:		print(e)