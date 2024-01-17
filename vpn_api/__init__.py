import datetime

from outline_vpn.outline_vpn import OutlineVPN

from database import Database

SUBSCRIPTIONS_TYPES = {
    'FREE_PLAN': 32_212_254_720,
    'FIRST_PLAN': 75_161_927_680,
    'SECOND_PLAN': 128_849_018_880,
    'MAX_PLAN': 536_870_912_000
}


class VPN_API:
    def __init__(self):
        self.client = OutlineVPN(api_url="https://85.234.106.236:59475/irCF-gdGLri3hIwh_0t-Xg",
                                 cert_sha256="1568E062F9A5E5FC58F725B5BB05CD4491972FB0CD80BA30F594BAC920BE1DF1")
        self.db = Database()
        self.key = None

    def new_key(self, user_id, sub_plan):
        # Create new key
        self.key = self.client.create_key(user_id)

        # Add data limit
        self.client.add_data_limit(self.key.key_id, SUBSCRIPTIONS_TYPES[sub_plan])

        # Add key data in DB
        insert_query = f"""
            INSERT INTO vpn_bot.keys (key_id, user_id, name, password, access_url, used_bytes, data_limit, reg_time)
            VALUES ('{self.key.key_id}', '{user_id}', '{self.key.name}', '{self.key.password}', '{self.key.access_url}', '{self.key.used_bytes}', '{SUBSCRIPTIONS_TYPES[sub_plan]}', '{datetime.datetime.now()}');
        """

        # Выполняем запрос
        self.db.execute(insert_query)

        return self.key.access_url



# data = VPN_API().client.get_keys()
# print(data)
# for key in data:
#     print(key)




# Get all access URLs on the server
# for key in client.get_keys():
#     print(key)

# # Create a new key
# new_key = client.create_key()
#
# # Rename it
# client.rename_key(new_key.key_id, "new_key")
#
# # Delete it
# client.delete_key(new_key.key_id)
#
# # Set a monthly data limit for a key (20MB)
# client.add_data_limit(new_key.key_id, 1000 * 1000 * 20)
#
# # Remove the data limit
# client.delete_data_limit(new_key.key_id)
