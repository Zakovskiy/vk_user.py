import vkuser;

vk = vkuser.Client("token");

while 1:

	result = vk.listen();

	if(result["type"] == "message_new"):

		content, peer_id, from_id = result["content"], result["peer_id"], result["from_id"];

		args = content.split(" ");

		if args[0] == "привет":
			vk.send_message("ку!", peer_id)["response"];