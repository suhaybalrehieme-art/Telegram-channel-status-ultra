import asyncio
import random
from telethon import TelegramClient, types, functions
from datetime import datetime

api_id = ********* 
api_hash = '**************************************'
channel_username = 'channel_user'

client = TelegramClient('stats1_session', api_id, api_hash)

async def main():
    async with client:
        entity = await client.get_entity(channel_username)
        full_channel = await client(functions.channels.GetFullChannelRequest(entity))
        subscribers_count = full_channel.full_chat.participants_count

        total_posts = 0
        total_views = 0
        total_forwards = 0
        max_views = 0
        top_post_id = 0
        total_stars = 0

        media_stats = {"صور": 0, "فيديوهات": 0, "ملفات": 0, "صوت": 0, "روابط": 0, "نصوص": 0}
        reaction_counts = {}
        first_post_date = None

        async for message in client.iter_messages(entity, reverse=True):
            if not first_post_date:
                first_post_date = message.date

            total_posts += 1
            views = (message.views or 0)
            total_views += views
            total_forwards += (message.forwards or 0)

            if views >= max_views:
                max_views = views
                top_post_id = message.id

            if message.reactions:
                for r in message.reactions.results:
                    if isinstance(r.reaction, types.ReactionPaid):
                        total_stars += r.count
                    elif hasattr(r.reaction, 'emoticon'):
                        emo = r.reaction.emoticon
                        reaction_counts[emo] = reaction_counts.get(emo, 0) + r.count
                    elif hasattr(r.reaction, 'document_id'):
                        reaction_counts["إيموجي مخصص"] = reaction_counts.get("إيموجي مخصص", 0) + r.count

            if message.photo: media_stats["صور"] += 1
            elif message.video: media_stats["فيديوهات"] += 1
            elif message.document: media_stats["ملفات"] += 1
            elif message.voice or message.audio: media_stats["صوت"] += 1
            elif not message.media: media_stats["نصوص"] += 1

            if message.entities:
                for e in message.entities:
                    if isinstance(e, (types.MessageEntityUrl, types.MessageEntityTextUrl)):
                        media_stats["روابط"] += 1
                        break

            if total_posts % 100 == 0:
                await asyncio.sleep(random.uniform(0.5, 1.0))

        avg_views = total_views / total_posts if total_posts > 0 else 0
        top_post_url = f"https://t.me/{channel_username}/{top_post_id}"

        report = (
            f"📊 تقرير لقناة: @{channel_username}\n"
            f"{'='*45}\n"
            f"👥 عدد المشتركين الحالي: {subscribers_count:,}\n"
            f"📅 تاريخ التأسيس المقدر: {first_post_date.strftime('%Y-%m-%d')}\n"
            f"📝 إجمالي عدد المنشورات: {total_posts:,}\n"
            f"🌟 إجمالي نجوم تيليجرام: {total_stars:,}\n"
            f"{'-'*45}\n"
            f"👁‍🗨 إجمالي المشاهدات: {total_views:,}\n"
            f"📈 متوسط المشاهدات لكل منشور: {avg_views:.2f}\n"
            f"🔄 إجمالي المشاركات (Forwards): {total_forwards:,}\n"
            f"{'-'*45}\n"
            f"🏆 المنشور الأكثر مشاهدة: {max_views:,} مشاهدة\n"
            f"🔗 رابط المنشور: {top_post_url}\n"
            f"{'-'*45}\n"
            f"📂 توزيع أنواع المحتوى:\n"
        )

        for key, value in media_stats.items():
            report += f" - {key}: {value}\n"

        report += f"{'-'*45}\n"
        report += "✨ تفاعلات المتابعين:\n"

        sorted_reactions = sorted(reaction_counts.items(), key=lambda x: x[1], reverse=True)
        for emo, count in sorted_reactions:
            report += f" {emo} : {count}\n"

        file_name = f"final_report_{channel_username}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(report

client.loop.run_until_complete(main())
