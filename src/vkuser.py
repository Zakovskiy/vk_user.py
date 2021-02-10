import requests
import json
import random

class Client():

	"""
		peer_id или chat_id можно узнать через метод get_dialogs();
		peer_id = chat_id + 2000000000
		chat_id = peer_id - 2000000000
	"""


	'''
    	-> параметр "access_token" -- VK User Token - можно получить здесь - https://oauth.vk.com/authorize?client_id=6121396&scope=501198815&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
    '''
	def __init__(self, access_token:str=None, version_api:str="5.126"):
		if access_token == None:
			exit("Empty param = `access_token`");
		else:
			self.access_token = access_token;
			self.v			  = version_api;
			self.get_longpoll_server();


	def get_longpoll_server(self):
		res = requests.get(f"https://api.vk.com/method/messages.getLongPollServer?access_token={self.access_token}&v={self.v}&need_pts=1&lp_version=3").json()["response"];
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

	# messages methods {

	def get_dialogs(self, offset:int=0, count:int=10):
		res = self.req("messages.getConversations", {"offset":offset, "count":count});
		return res;

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
		res = self.req("messages.getConversationMembers", {"peer_id":peer_id})

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

	def send_message(self, content:str = "я фан зака..", peer_id:int = 2000000000):
		data = {
			"random_id":random.randint(100000000, 900000000),
			"message":content
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
