# METADATA

- 66b1675a14ce16db6476210b5e95d2eff00f58f9
- [Milky](https://raw.githubusercontent.com/SaltifyDev/milky/refs/heads/main/packages/types/src/api-endpoints.ts)
- 4c401e3a6615375de606e488b9288f11b534c73a
- [NapCat](https://raw.githubusercontent.com/NapNeko/NapCatDocs/refs/heads/main/src/develop/api.md)

## 🧩 Milky ↔ NapCat 接口对照表

| **接口说明**           | **Milky 接口**                     | **NapCat 接口**                                                      |
| ---------------------- | ---------------------------------- | -------------------------------------------------------------------- |
| 获取登录信息           | get_login_info                     | get_login_info                                                       |
| 获取协议端信息         | get_impl_info                      | 无                                                                   |
| 获取用户个人信息       | get_user_profile                   | get_stranger_info                                                    |
| 获取好友列表           | get_friend_list                    | get_friend_list                                                      |
| 获取好友信息           | get_friend_info                    | get_stranger_info                                                    |
| 获取群列表             | get_group_list                     | get_group_list                                                       |
| 获取群信息             | get_group_info                     | get_group_info                                                       |
| 获取群成员列表         | get_group_member_list              | get_group_member_list                                                |
| 获取群成员信息         | get_group_member_info              | get_group_member_info                                                |
| 获取 Cookies           | get_cookies                        | get_cookies                                                          |
| 获取 CSRF Token        | get_csrf_token                     | get_csrf_token                                                       |
| 发送私聊消息           | send_private_message               | send_private_msg                                                     |
| 发送群聊消息           | send_group_message                 | send_group_msg                                                       |
| 通用发送消息           | 无                                 | send_msg                                                             |
| 撤回私聊消息           | recall_private_message             | delete_msg                                                           |
| 撤回群聊消息           | recall_group_message               | delete_msg                                                           |
| 获取消息详情           | get_message                        | get_msg                                                              |
| 获取历史消息           | get_history_messages               | get_group_msg_history / get_friend_msg_history                       |
| 获取临时资源链接       | get_resource_temp_url              | 无                                                                   |
| 获取合并转发消息       | get_forwarded_messages             | get_forward_msg                                                      |
| 标记消息为已读         | mark_message_as_read               | mark_private_msg_as_read / mark_group_msg_as_read / mark_msg_as_read |
| 好友戳一戳             | send_friend_nudge                  | friend_poke / send_poke                                              |
| 群聊戳一戳             | send_group_nudge                   | group_poke / send_poke                                               |
| 发送名片点赞           | send_profile_like                  | send_like                                                            |
| 获取好友请求           | get_friend_requests                | get_friend_requests                                                  |
| 同意好友请求           | accept_friend_request              | set_friend_add_request                                               |
| 拒绝好友请求           | reject_friend_request              | set_friend_add_request                                               |
| 设置群名称             | set_group_name                     | set_group_name                                                       |
| 设置群头像             | set_group_avatar                   | set_group_portrait                                                   |
| 设置群成员名片         | set_group_member_card              | set_group_card                                                       |
| 设置群成员头衔         | set_group_member_special_title     | set_group_special_title                                              |
| 设置群管理员           | set_group_member_admin             | set_group_admin                                                      |
| 设置群成员禁言         | set_group_member_mute              | set_group_ban                                                        |
| 设置群全员禁言         | set_group_whole_mute               | set_group_whole_ban                                                  |
| 踢出群成员             | kick_group_member                  | set_group_kick                                                       |
| 获取群公告             | get_group_announcements            | \_get_group_notice / get_group_announcement                          |
| 发送群公告             | send_group_announcement            | \_send_group_notice / send_group_announcement                        |
| 删除群公告             | delete_group_announcement          | \_del_group_notice / del_group_announcement                          |
| 获取群精华消息         | get_group_essence_messages         | get_essence_msg_list                                                 |
| 设置群精华消息         | set_group_essence_message          | set_essence_msg                                                      |
| 删除精华消息           | set_group_essence_message 传参实现 | delete_essence_msg                                                   |
| 退出群聊               | quit_group                         | set_group_leave                                                      |
| 群消息表情回应         | send_group_message_reaction        | set_msg_emoji_like                                                   |
| 获取群通知             | get_group_notifications            | get_group_system_msg                                                 |
| 同意入群请求           | accept_group_request               | set_group_add_request                                                |
| 拒绝入群请求           | reject_group_request               | set_group_add_request                                                |
| 同意群邀请             | accept_group_invitation            | accept_group_invitation                                              |
| 拒绝群邀请             | reject_group_invitation            | reject_group_invitation                                              |
| 上传私聊文件           | upload_private_file                | upload_private_file                                                  |
| 上传群文件             | upload_group_file                  | upload_group_file                                                    |
| 获取私聊文件下载链接   | get_private_file_download_url      | get_file                                                             |
| 获取群文件下载链接     | get_group_file_download_url        | get_group_file_url                                                   |
| 获取群文件列表         | get_group_files                    | get_group_files / get_group_root_files                               |
| 移动群文件             | move_group_file                    | move_group_file                                                      |
| 重命名群文件           | rename_group_file                  | rename_group_file                                                    |
| 删除群文件             | delete_group_file                  | delete_group_file                                                    |
| 创建群文件夹           | create_group_folder                | create_group_file_folder                                             |
| 重命名群文件夹         | rename_group_folder                | rename_group_folder                                                  |
| 删除群文件夹           | delete_group_folder                | delete_group_folder                                                  |
| 下载文件到缓存         | 无                                 | download_file                                                        |
| 获取群文件系统信息     | 无                                 | get_group_file_system_info                                           |
| 获取群子目录文件       | 无                                 | get_group_files_by_folder                                            |
| 获取群荣誉信息         | 无                                 | get_group_honor_info                                                 |
| 获取 QQ 凭证           | 无                                 | get_credentials                                                      |
| 获取语音               | 无                                 | get_record                                                           |
| 获取图片               | 无                                 | get_image                                                            |
| 检查是否可发语音       | 无                                 | can_send_record                                                      |
| 检查是否可发图片       | 无                                 | can_send_image                                                       |
| 图片 OCR               | 无                                 | ocr_image                                                            |
| 获取运行状态           | 无                                 | get_status                                                           |
| 获取版本信息           | 无                                 | get_version_info                                                     |
| 清理缓存               | 无                                 | clean_cache                                                          |
| 检查链接安全性         | 无                                 | check_url_safely                                                     |
| 快速操作               | 无                                 | handle_quick_operation                                               |
| 获取 @全体 剩余次数    | 无                                 | get_group_at_all_remain                                              |
| 群打卡                 | 无                                 | send_group_sign                                                      |
| 设置群签名             | 无                                 | set_group_sign                                                       |
| Ark 分享到私聊         | 无                                 | ArkSharePeer                                                         |
| Ark 分享到群聊         | 无                                 | ArkShareGroup                                                        |
| 获取机器人 QQ 区间     | 无                                 | get_robot_uin_range                                                  |
| 设置在线状态           | 无                                 | set_online_status                                                    |
| 获取好友分组           | 无                                 | get_friends_with_category                                            |
| 设置 QQ 头像           | 无                                 | set_qq_avatar                                                        |
| 转发单条消息到私聊     | 无                                 | forward_friend_single_msg                                            |
| 转发单条消息到群聊     | 无                                 | forward_group_single_msg                                             |
| 创建文本收藏           | 无                                 | create_collection                                                    |
| 获取收藏列表           | 无                                 | get_collection_list                                                  |
| 设置个人签名           | 无                                 | set_self_longnick                                                    |
| 获取最近联系人         | 无                                 | get_recent_contact                                                   |
| 标记所有为已读         | 无                                 | \_mark_all_as_read                                                   |
| 获取点赞列表           | 无                                 | get_profile_like                                                     |
| 获取收藏表情           | 无                                 | fetch_custom_face                                                    |
| 获取表情回应           | 无                                 | fetch_emoji_like                                                     |
| 设置输入状态           | 无                                 | set_input_status                                                     |
| 获取群扩展信息         | 无                                 | get_group_info_ex                                                    |
| 获取忽略加群请求       | 无                                 | get_group_ignore_add_request                                         |
| 获取 PacketServer 状态 | 无                                 | nc_get_packet_status                                                 |
| 获取陌生人在线状态     | 无                                 | nc_get_user_status                                                   |
| 获取 Rkey              | 无                                 | nc_get_rkey                                                          |
| 获取小程序卡片         | 无                                 | get_mini_app_ark                                                     |
| 获取 AI 语音记录       | 无                                 | get_ai_record                                                        |
| 获取 AI 角色列表       | 无                                 | get_ai_characters                                                    |
| 发送 AI 语音到群聊     | 无                                 | send_group_ai_record                                                 |
| 获取群禁言成员列表     | 无                                 | get_group_shut_list                                                  |

---

如需导出为 CSV 或继续补充说明字段，我可以继续帮你完善。是否还需要按分类拆分或补充结构体信息？
