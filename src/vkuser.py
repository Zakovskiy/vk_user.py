import requests
import json
import random
import base64
class Client():

	"""
		peer_id или chat_id можно узнать через метод get_dialogs();
		peer_id = chat_id + 2000000000
		chat_id = peer_id - 2000000000
	"""


	'''
		-> параметр "access_token" -- VK User Token - можно получить здесь - https://oauth.vk.com/authorize?client_id=6121396&scope=501198815&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
		-> параметр "type"		   -- False - токен группы, True - токен юзера.
	'''
	def __init__(self, access_token:str=None, version_api:str="5.126", type=True, group_id:int = None):
		if access_token == None:
			exit("Empty param = `access_token`");
		else:
			self.access_token = access_token;
			self.v			  = version_api;
			self.type		  = type;
			if not type and not group_id:
				exit("Empty param = `group_id`");
			self.group_id = group_id;
			self.get_longpoll_server();


	def get_longpoll_server(self):
		if self.type:
			res = requests.get(f"https://api.vk.com/method/messages.getLongPollServer?access_token={self.access_token}&v={self.v}&need_pts=1&lp_version=3").json()["response"];
		else:
			res = requests.get(f"https://api.vk.com/method/groups.getLongPollServer?access_token={self.access_token}&v={self.v}&group_id={self.group_id}").json()["response"];
		self.server = res["server"];
		self.key    = res["key"];
		self.ts     = res["ts"];
		return res;

	# account methods {

	def set_online(self):
		res = self.req("account.setOnline", {});
		return res

	def set_offline(self):
		res = self.req("account.setOffline", {});
		return res

	def get_profile_info(self):
		res = self.req("account.getProfileInfo",{});
		return res;

	def get_info(self, user_id:int=1):
		res = self.req("account.getInfo",{"user_id":user_id});
		return res;

	def ban(self, user_id:int=1):
		res = self.req("account.ban", {"owner_id":user_id});
		return res;

	def unban(self, user_id:int=1):
		res = self.req("account.unban", {"owner_id":user_id});
		return res;

	def get_banned_list(self, offset:int=0, count:int=200):
		res = self.req("account.getBanned", {"offset":offset, "count":count});
		return res;

	def get_app_permissions(self):
		res = self.req("account.getAppPermissions", {});
		return res;

	# }

	# gifts methods {

	def get_gifts(self, user_id:int = None):
		res = self.req("gifts.get", {"user_id":user_id});
		return res;

	# }

	# likes methods {

	def add_like(self, type:str = "post", owner_id:int=1, item_id:int=1):
		res = self.req("likes.add", {"type":type, "owner_id":owner_id, "item_id":item_id});
		return res;

	def delete_like(self, type:str = "post", owner_id:int=1, item_id:int=1):
		res = self.req("likes.delete", {"type":type, "owner_id":owner_id, "item_id":item_id});
		return res;

	def list_like(self, type:str = "post", owner_id:int=1, item_id:int=1):
		res = self.req("likes.getList", {"type":type, "owner_id":owner_id, "item_id":item_id});
		return res;

	def is_like(self, type:str = "post", owner_id:int=1, item_id:int=1, user_id:int=2):
		res = self.req("likes.getList", {"type":type, "owner_id":owner_id, "item_id":item_id, "user_id":user_id});
		return res;

	# }

	# return new message {
	def listen(self):
		if self.type:
			res = requests.get(f"https://{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25&mode=2&version=3").json();
			self.ts = res["ts"];
			if len(res["updates"]) == 0:
				return {"type":"empty"}
			else:
				if res["updates"][0][0] == 4:
					data = {
						"type":"message_new",
						"peer_id":res["updates"][0][3],
						"content":res["updates"][0][5],
						"from_id": res["updates"][0][6]["from"] if "from" in res["updates"][0][6] else None
					}
				else:
					data = {"type":"unknown", "c":res["updates"]};
		else:
			res = requests.get(f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=25").json();
			try:
				self.ts = res["ts"];
			except:
				print(res);
			if len(res["updates"]) == 0:
				return {"type":"empty"}
			else:
				data = res["updates"][0];
		return data;
	# }

	# wall methods {

	def close_comments(self, post_id:int=1, owner_id:int=1):
		res = self.req("wall.closeComments", {"post_id":post_id, "owner_id":owner_id});
		return res;

	def open_comments(self, post_id:int=1, owner_id:int=1):
		res = self.req("wall.openComments", {"post_id":post_id, "owner_id":owner_id});
		return res;

	def create_comment(self, message:str="я фан зака", post_id:int=1, owner_id:int=1):
		res = self.req("wall.createComment", {"message":message, "post_id":post_id, "owner_id":owner_id});
		return res;

	def delete_comment(self, comment_id:int=1, owner_id:int=1):
		res = self.req("wall.deleteComment", {"comment_id":comment_id, "owner_id":owner_id});
		return res;

	def delete_wall(self, post_id:int=1, owner_id:int=1):
		res = self.req("wall.delete", {"post_id":post_id, "owner_id":owner_id});
		return res;

	def get_wall(self, owner_id:int=1, offset:int=0, count:int=100):
		res = self.req("wall.get", {"owner_id":owner_id, "offset":offset, "count":count});
		return res;

	def pin_wall(self, post_id:int=1, owner_id:int=1):
		res = self.req("wall.pin", {"post_id":post_id, "owner_id":owner_id});
		return res;

	def get_comments(self, post_id:int=1, owner_id:int=1, offset:int=0, count:int=100):
		res = self.req("wall.getComments", {"post_id":post_id, "owner_id":owner_id, "offset":offset, "count":count});
		return res;

	# }

	# users methods {

	def get_users(self, user_ids:str="1, 2", fields:str = None):
		res = self.req("users.get", {"user_ids":user_ids, "fields":fields});
		return res;

	def get_followers(self, user_id:int=1, offset:int=0, count:int=1000):
		res = self.req("users.getFollowers", {"user_id":user_id, "offset":offset, "count":count});
		return res;

	def get_subscriptions(self, user_id:int=1, offset:int=0, count:int=1000):
		res = self.req("users.getSubscriptions", {"user_id":user_id, "offset":offset, "count":count});
		return res;

	def report_user(self, user_id:int=1, type:str="spam", comment:str = None):
		res = self.req("users.report", {"user_id":user_id, "type":type, "comment":comment});
		return res;

	# }

	# status methods {

	def get_status(self, user_id:int=1):
		res = self.req("status.get", {"user_id":user_id});
		return res;

	def set_status(self, text:str="я фан зака"):
		res = self.req("status.set", {"text":text});
		return res;

	# }

	# photos methods {

	def get_upload_server_photo(self, peer_id:int=0):
		res = self.req("photos.getMessagesUploadServer", {"peer_id":peer_id})["response"];
		return res;

	def upload_photo(self, image, upload_url):
		with FilesOpener(image) as img: 
			res = requests.post(upload_url, files=img).json();
		return res;

	def save_messages_photo(self, photo, server, hash):
		return self.req("photos.saveMessagesPhoto", {"photo":photo, "server":server, "hash":hash})["response"][0];

	# }

	# messages methods {

	def get_dialogs(self, offset:int=0, count:int=10):
		res = self.req("messages.getConversations", {"offset":offset, "count":count});
		return res;

	def send_image(self, content:str=None, img:str="", peer_id:int=0):
		gusp = self.get_upload_server_photo(peer_id=peer_id);
		up   = self.upload_photo(image=img, upload_url=gusp["upload_url"]);
		smp  = self.save_messages_photo(up["photo"], up["server"], up["hash"]);

		return self.send_message(content=content,peer_id=peer_id, attachment=f"photo{smp['owner_id']}_{smp['id']}")

	def create_chat(self, title:str="фан беседа зака", user_ids:str="1, 2, 3"):
		res = self.req("messages.createChat", {"user_ids":user_ids, "title":title});
		return res;

	def get_history(self, peer_id:int=2000000000):
		res = self.req("messages.getHistory", {"peer_id":peer_id});
		return res;

	def get_history_attachments(self, peer_id:int=2000000000):
		res = self.req("messages.getHistoryAttachments", {"peer_id":peer_id});
		return res;

	def get_important_messages(self, count:int=200):
		res = self.req("messages.getImportantMessages", {"count":count});
		return res;

	def typing(self, peer_id:int=2000000000):
		res = self.req("messages.setActivity", {"peer_id":peer_id});
		return res;

	def get_last_activity(self, user_id:int=1):
		res = self.req("messages.getLastActivity", {"user_id":user_id});
		return res;

	def join_chat_by_link(self, link:str=None):
		res = self.req("messages.joinChatByInviteLink", {"link":link});
		return res;

	def get_chat_info(self, chat_id:int=0):
		res = self.req("messages.getChat", {"chat_id":chat_id});
		return res;

	def get_chat_members(self, peer_id:int=2000000000):
		res = self.req("messages.getConversationMembers", {"peer_id":peer_id});
		return res;

	def edit_chat(self, title:str="фан беседа зака", chat_id:int=0):
		res = self.req("messages.editChat", {"chat_id":chat_id, "title":title});
		return res;

	def get_invite_link(self, peer_id:int=0, reset:int=0):
		res = self.req("messages.getInviteLink",{"peer_id":peer_id, "reset":reset});
		return res;

	def add_chat_user(self, chat_id:int=0, user_id:int=1, visible_messages_count:int=3):
		res = self.req("messages.addChatUser",{"chat_id":chat_id, "user_id":user_id, "visible_messages_count":visible_messages_count});
		return res;

	def get_chat_preview(self, peer_id:int=2000000000):
		res = self.req("messages.getChatPreview", {"peer_id":peer_id});
		return res;

	def delete_chat_photo(self, chat_id:int=0):
		res = self.req("messages.deleteChatPhoto", {"chat_id":chat_id});
		return res;

	def delete_message(self, message_ids:str="1, 2", delete_for_all:bool=True):
		res = self.req("messages.delete", {"message_id":message_ids, "delete_for_all":1 if delete_for_all else 0});
		return res

	def pin_message(self, peer_id:int=2000000000,message_id:int=0):
		res = self.req("messages.pin", {"peer_id":peer_id, "message_id":message_id});
		return res;

	def remove_chat_user(self, chat_id:int=0, user_id:int=1):
		res = self.req("messages.removeChatUser", {"chat_id":chat_id, "user_id":user_id});
		return res;

	def send_message(self, content:str = "я фан зака..", peer_id:int = 2000000000, **kwargs):
		data = {
			"random_id":random.randint(100000000, 900000000),
			"message":content,
			**kwargs
		}
		if peer_id < 2000000000:
			data["user_id"] = peer_id;
		else:
			data["peer_id"] = peer_id;
		res = self.req("messages.send", data);
		return res;

	def edit_message(self, content:str = "?", peer_id:int=2000000000, message_id:int=0):
		data = {
			"message":content,
			"message_id":message_id,
		};
		data["peer_id"] = peer_id;

		res = self.req("messages.edit",data)
		return res;

	# }


	def req(self, req, params):
		params["access_token"] = self.access_token;
		params["v"]			   = self.v;
		res 				   = requests.post(f"https://api.vk.com/method/{req}/", data=params).json();
		return res;

class FilesOpener(object):
	def __init__(self, paths, key_format='file{}'):
		if not isinstance(paths, list):
			paths = [paths]

		self.paths = paths
		self.key_format = key_format
		self.opened_files = []

	def __enter__(self):
		return self.open_files()

	def __exit__(self, type, value, traceback):
		self.close_files()

	def open_files(self):
		self.close_files()

		files = []

		for x, file in enumerate(self.paths):
			if hasattr(file, 'read'):
				f = file

				if hasattr(file, 'name'):
					filename = file.name
				else:
					filename = '.jpg'
			else:
				filename = file
				f = open(filename, 'rb')
				self.opened_files.append(f)

			ext = filename.split('.')[-1]
			files.append(
				(self.key_format.format(x), ('file{}.{}'.format(x, ext), f))
			)

		return files

	def close_files(self):
		for f in self.opened_files:
			f.close()

		self.opened_files = []
