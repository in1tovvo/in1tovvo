-- PostgreSQL 数据库初始化脚本
-- 生成时间: 2026-03-18 16:01:12
-- 适用于 Neon PostgreSQL

-- 注意：users 表的密码哈希可能需要重新生成（werkzeug）

-- =========== 表: settings ===========
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- 插入 settings 数据
INSERT INTO settings (key, value) VALUES ('wedding_date', '2026-09-28');

-- =========== 表: tasks ===========
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    phase TEXT,
    due_date DATE,
    assigned_to TEXT,
    status TEXT,
    priority TEXT,
    reference_id TEXT,
    dependencies TEXT,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    is_needed BOOLEAN
);

-- 插入 tasks 数据
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (9, '确定婚礼预算总额', '包括：场地、餐饮、摄影、摄像、化妆、婚纱、策划等各项预算分配', '预算', '18-12个月', '2025-09-18', '', 'pending', 'critical', 'budget_total', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (10, '初步确定婚礼日期', '避开重要节日/家庭忌日，考虑季节、天气、场地 availability', '日程', '18-12个月', '2025-10-08', '', 'pending', 'critical', 'wedding_date', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (11, '订婚仪式（如需要）', '传统订婚习俗，双方家庭见面', '仪式', '18-12个月', '2025-10-28', '', 'pending', 'low', 'engagement', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (12, '搜集婚礼灵感', 'Pinterest、小红书、婚礼纪等平台收集婚礼风格、布置、造型灵感', '策划', '18-12个月', '2025-11-17', '', 'pending', 'low', 'inspiration_collect', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (13, '确定婚礼主题与色调', '中式/西式/森系/海洋/复古等主题，确定主色调', '策划', '18-12个月', '2025-12-07', '', 'pending', 'high', 'wedding_theme', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (14, '寻找并确定婚礼策划师', '查看案例、对比报价、签订合同', '婚庆', '18-12个月', '2025-12-17', '', 'pending', 'high', 'planner_select', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (15, '初步拟定宾客名单', '两大阵营（男方、女方）分别列出，估算人数', '宾客', '18-12个月', '2025-12-27', '', 'pending', 'high', 'guest_list_draft', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (16, '开始了解婚礼场地', '酒店、户外草坪、特色场地等，确定餐标和容纳人数', '场地', '18-12个月', '2026-01-06', '', 'pending', 'high', 'venue_research', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (17, '预订婚礼场地', '签订合同、支付定金、确定婚礼日期和人数上限', '场地', '12-9个月', '2026-03-17', '', 'pending', 'critical', 'venue_booking', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (18, '确定并签约婚庆策划公司', '确认策划方案、布置效果图、人员配置', '婚庆', '12-9个月', '2026-04-06', '', 'pending', 'critical', 'planner_confirm', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (19, '预订婚纱摄影', '确定摄影风格、套餐、拍摄日期（含旅拍）', '摄影', '12-9个月', '2026-04-16', '', 'pending', 'high', 'photography_booking', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (20, '预订新娘婚纱/礼服', '试穿、定制或租赁，包括出门纱、主纱、敬酒服', '服装', '12-9个月', '2026-04-26', '', 'pending', 'high', 'wedding_dress', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (21, '预订新郎西装/礼服', '定制或购买，需多次试穿修改', '服装', '12-9个月', '2026-04-26', '', 'pending', 'medium', 'groom_suit', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (22, '预订婚礼主持/司仪', '查看主持案例，确定风格（幽默/温馨/庄严）', '人员', '12-9个月', '2026-05-06', '', 'pending', 'high', 'mc_booking', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (23, '预订化妆师', '新娘妆、妈妈妆，需试妆确定妆容', '人员', '12-9个月', '2026-05-16', '', 'pending', 'high', 'makeup_booking', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (24, '开始搜集婚戒/首饰', '了解钻石4C标准、戒指款式、品牌对比', '首饰', '12-9个月', '2026-05-26', '', 'pending', 'medium', 'ring_research', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (25, '确定婚礼流程方案', '与策划师确认婚礼当天详细流程表', '策划', '9-6个月', '2026-06-15', '', 'pending', 'high', 'flow_confirm', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (26, '预订婚宴菜单和酒水', '试菜、确定菜单、酒水数量', '餐饮', '9-6个月', '2026-06-25', '', 'pending', 'high', 'menu_confirm', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (27, '预订婚礼摄像', '视频跟拍、快剪、完整纪录片', '摄像', '9-6个月', '2026-07-05', '', 'pending', 'medium', 'videography_booking', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (28, '预订婚礼 DJ/灯光音响', '音乐DJ、灯光效果、音响设备', '设备', '9-6个月', '2026-07-15', '', 'pending', 'medium', 'dj_lighting', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (29, '预订婚车', '头车（豪车）+跟车，确定路线、司机', '交通', '9-6个月', '2026-07-25', '', 'pending', 'medium', 'wedding_car', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (30, '购买结婚戒指/首饰', '对戒、求婚戒指、 Wedding Band', '首饰', '9-6个月', '2026-08-04', '', 'pending', 'high', 'jewelry_buy', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (31, '选购婚礼甜品台/蛋糕', '甜品台设计、蛋糕定制、试吃', '餐饮', '9-6个月', '2026-08-14', '', 'pending', 'low', 'dessert_booking', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (32, '预订鲜花/花艺布置', '手捧花、胸花、桌花、仪式区、迎宾区花艺', '鲜花', '9-6个月', '2026-08-24', '', 'pending', 'high', 'floral_design', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (33, '发送正式请柬', '电子+纸质请柬，通知婚礼详情', '请柬', '6-3个月', '2026-09-13', '', 'pending', 'high', 'invitation_send', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (34, '确认伴郎伴娘并通知', '确定人员名单、准备服装、安排任务', '人员', '6-3个月', '2026-09-23', '', 'pending', 'medium', 'bridesmaids_groomsmen', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (35, '新郎新娘试妆', '确定婚礼当天造型，试假发、妆面', '美容', '6-3个月', '2026-10-03', '', 'pending', 'high', 'makeup_trial', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (36, '新娘婚纱试穿并修改', '多次试穿、调整尺寸、确定最终版', '服装', '6-3个月', '2026-10-13', '', 'pending', 'high', 'dress_fitting', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (37, '选购结婚对戒', '挑选对戒款式、刻字、size确认', '首饰', '6-3个月', '2026-10-23', '', 'pending', 'medium', 'wedding_ring', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (38, '安排蜜月旅行', '办理签证、预订机票酒店、规划行程', '旅行', '6-3个月', '2026-11-02', '', 'pending', 'medium', 'honeymoon', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (39, '选购新郎西装并试穿修改', '定制作或购买，需确保合身', '服装', '6-3个月', '2026-11-12', '', 'pending', 'medium', 'groom_suit_fitting', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (40, '准备婚房布置', '采购装饰品、喜字、拉花、气球等', '婚房', '6-3个月', '2026-11-22', '', 'pending', 'low', 'home_decoration', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (41, '收集宾客回执并统计最终人数', '整理最终确认名单，区分必到和可能到', '宾客', '3-1个月', '2026-12-12', '', 'pending', 'critical', 'guest_confirmation', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (42, '与策划师确认婚礼详细流程表', '时间轴、环节衔接、人员分工', '策划', '3-1个月', '2026-12-22', '', 'pending', 'high', 'flow_finalize', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (43, '确认婚宴最终菜单和酒水数量', '根据确认人数调整菜品、酒水', '餐饮', '3-1个月', '2027-01-01', '', 'pending', 'high', 'menu_final', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (44, '安排住宿和交通', '外地宾客住宿、婚车、接送安排', '交通', '3-1个月', '2027-01-11', '', 'pending', 'medium', 'transportation', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (45, '购买伴手礼/宾客回礼', '选择礼品、定制包装、分装', '礼品', '3-1个月', '2027-01-21', '', 'pending', 'medium', 'wedding_favors', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (46, '准备婚礼红包', '不同面额、数量充足，准备专用红包袋', '红包', '3-1个月', '2027-01-31', '', 'pending', 'high', 'red_packets', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (47, '新娘美容护理', '皮肤管理、脱毛、牙齿美白等', '美容', '3-1个月', '2027-02-10', '', 'pending', 'medium', 'beauty_care', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (48, '最终彩排', '全体人员走台、熟悉流程', '彩排', '3-1个月', '2027-02-20', '', 'pending', 'high', 'rehearsal', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (49, '准备婚礼当天物品清单', '应急包、备用物品、重要文件', '物资', '3-1个月', '2027-02-25', '', 'pending', 'high', 'emergency_kit', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (50, '分发座位表给酒店/策划师', '最终座位安排，打印席位卡', '宾客', '1-0周', '2027-03-05', '', 'pending', 'high', 'seating_chart', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (51, '最终确认供应商到场时间和细节', '拍照、电话确认所有供应商', '供应商', '1-0周', '2027-03-07', '', 'pending', 'critical', 'vendor_confirm', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (52, '新娘美甲、美发、全身护理', '婚礼前最后的美容护理', '美容', '1-0周', '2027-03-09', '', 'pending', 'medium', 'final_beauty', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (53, '准备应急包', '针线、备用高跟鞋、创可贴、止痛药、充电宝等', '物资', '1-0周', '2027-03-10', '', 'pending', 'high', 'emergency_pack', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (54, '分装红包、伴手礼、喜糖', '按桌或按人分装', '物资', '1-0周', '2027-03-10', '', 'pending', 'medium', 'gift_packing', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (55, '贵重物品、合同、现金交接', '交给信任的亲友保管', '财务', '1-0周', '2027-03-11', '', 'pending', 'high', 'valuables', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (56, '早点休息，放松心情', '保证充足睡眠，为婚礼储备精力', '健康', '1-0周', '2027-03-11', '', 'pending', 'critical', 'rest', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (57, '早起洗漱、吃早餐', '保持体力，简单早餐', '流程', '婚礼当天', NULL, '', 'pending', 'critical', 'wedding_day_breakfast', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (58, '新娘化妆、做发型', '化妆师到位，全程约2-3小时', '美容', '婚礼当天', NULL, '', 'pending', 'high', 'bride_makeup', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (59, '新郎剃须、做发型', '新郎准备，可拍摄花絮', '美容', '婚礼当天', NULL, '', 'pending', 'medium', 'groom_grooming', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (60, '接亲游戏（堵门、找鞋、敬茶）', '传统接亲环节，安排游戏、红包', '环节', '婚礼当天', NULL, '', 'pending', 'high', 'door_game', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (61, '敬改口茶（收红包）', '向双方父母敬茶，改口收红包', '环节', '婚礼当天', NULL, '', 'pending', 'high', 'tea_ceremony', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (62, '新郎新娘出门、上车', '新娘出门，婚车队伍出发', '流程', '婚礼当天', NULL, '', 'pending', 'medium', 'departure', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (63, '迎宾/签到（引导宾客入座）', '在酒店门口迎宾，引导入座', '流程', '婚礼当天', NULL, '', 'pending', 'high', 'checkin', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (64, '婚礼仪式（入场、宣誓、交换戒指、抛花）', '婚礼核心仪式环节', '环节', '婚礼当天', NULL, '', 'pending', 'critical', 'ceremony', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (65, '婚宴敬酒（按桌敬酒、致辞）', '新人逐桌敬酒、父母致辞', '环节', '婚礼当天', NULL, '', 'pending', 'high', 'wedding_banquet', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (66, '送客/欢送宾客', '婚礼结束，欢送客人', '流程', '婚礼当天', NULL, '', 'pending', 'medium', 'farewell', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (67, '结算（酒店、供应商尾款）', '支付所有尾款，取回收据', '财务', '婚礼当天', NULL, '', 'pending', 'critical', 'settlement', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (68, '感谢宾客（发送感谢卡/微信）', '向出席的宾客表达感谢', '礼仪', '婚礼后1周', NULL, '', 'pending', 'medium', 'thank_guests', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (69, '整理婚礼照片/视频', '备份到云端，挑选精修', '纪念', '婚礼后1周', NULL, '', 'pending', 'low', 'photo_backup', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (70, '给供应商评价', '在婚礼纪、小红书、大众点评等平台评价', '售后', '婚礼后1周', NULL, '', 'pending', 'low', 'vendor_review', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (71, '整理婚礼物品', '婚纱、装饰品、剩余物品收纳', '整理', '婚礼后1周', NULL, '', 'pending', 'low', 'items_organize', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (72, '结算所有账单', '核对所有发票、付款、报销', '财务', '婚礼后1周', NULL, '', 'pending', 'high', 'final_settlement', NULL, '2026-03-12 00:49:20', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (73, '购买结婚对戒', '挑选对戒款式、刻字、size确认', '首饰', '9-6个月', '2026-08-03', '', 'pending', 'high', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (74, '预订婚车', '头车（豪车）+跟车，确定路线、司机', '交通', '9-6个月', '2026-07-24', '', 'pending', 'medium', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (75, '选购喜糖/伴手礼糖果', '采购喜糖、巧克力、定制包装盒', '礼品', '9-6个月', '2026-09-02', '', 'pending', 'medium', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (76, '取回结婚对戒', '确保戒指刻字正确、尺寸合适', '首饰', '6-3个月', '2026-11-11', '', 'pending', 'medium', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (77, '分装伴手礼/回礼', '按桌或按人分装伴手礼', '礼品', '3-1个月', '2027-01-30', '', 'pending', 'medium', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (78, '准备喜糖/糖果盒', '分装喜糖到每个宾客的糖果盒', '礼品', '3-1个月', '2027-02-14', '', 'pending', 'medium', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (79, '打印座位表和席位卡', '制作签到台座位表、每桌席位卡', '宾客', '1-0周', '2027-03-04', '', 'pending', 'high', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (80, '检查婚礼服装和配饰', '检查婚纱、西装、内衣、鞋、配饰是否齐全', '服装', '1-0周', '2027-03-07', '', 'pending', 'high', NULL, NULL, '2026-03-12 00:50:18', NULL, true);
INSERT INTO tasks (id, title, description, category, phase, due_date, assigned_to, status, priority, reference_id, dependencies, created_at, completed_at, is_needed) VALUES (81, '封装红包并指定保管人', '按用途分装红包，交给指定亲友', '财务', '1-0周', '2027-03-09', '', 'pending', 'high', NULL, NULL, '2026-03-12 00:50:18', NULL, true);

-- =========== 表: sqlite_sequence ===========
CREATE TABLE IF NOT EXISTS sqlite_sequence (
    name TEXT,
    seq TEXT
);

-- 插入 sqlite_sequence 数据
INSERT INTO sqlite_sequence (name, seq) VALUES ('tasks', 82);
INSERT INTO sqlite_sequence (name, seq) VALUES ('budget', 32);
INSERT INTO sqlite_sequence (name, seq) VALUES ('vendors', 8);
INSERT INTO sqlite_sequence (name, seq) VALUES ('moodboard', 6);
INSERT INTO sqlite_sequence (name, seq) VALUES ('tables', 20);
INSERT INTO sqlite_sequence (name, seq) VALUES ('guests', 2);
INSERT INTO sqlite_sequence (name, seq) VALUES ('guest_tables', 2);

-- =========== 表: budget ===========
CREATE TABLE IF NOT EXISTS budget (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    item_name TEXT NOT NULL,
    estimated_cost REAL,
    actual_cost REAL,
    deposit REAL,
    balance REAL,
    vendor TEXT,
    vendor_contact TEXT,
    contract_file TEXT,
    status TEXT,
    notes TEXT,
    created_at TIMESTAMP
);

-- =========== 表: guests ===========
CREATE TABLE IF NOT EXISTS guests (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    relationship TEXT,
    side TEXT,
    table_number INTEGER,
    invitation_status TEXT,
    rsvp_status TEXT,
    plus_one BOOLEAN,
    dietary_restrictions TEXT,
    gift_amount REAL,
    notes TEXT
);

-- 插入 guests 数据
INSERT INTO guests (id, name, phone, email, relationship, side, table_number, invitation_status, rsvp_status, plus_one, dietary_restrictions, gift_amount, notes) VALUES (1, 'test1', '', '', '', 'both', 0, 'pending', 'no_response', false, '', 0.0, '');
INSERT INTO guests (id, name, phone, email, relationship, side, table_number, invitation_status, rsvp_status, plus_one, dietary_restrictions, gift_amount, notes) VALUES (2, '2', '', '', '', 'both', 0, 'pending', 'no_response', false, '', 0.0, '');

-- =========== 表: vendors ===========
CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    price_range TEXT,
    rating REAL,
    notes TEXT,
    contract_date DATE,
    contract_file TEXT,
    created_at TIMESTAMP
);

-- =========== 表: moodboard ===========
CREATE TABLE IF NOT EXISTS moodboard (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT,
    image_url TEXT,
    tags TEXT,
    notes TEXT,
    created_at TIMESTAMP
);

-- =========== 表: tables ===========
CREATE TABLE IF NOT EXISTS tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER NOT NULL,
    table_name TEXT,
    shape TEXT,
    capacity INTEGER,
    x_coordinate REAL,
    y_coordinate REAL,
    notes TEXT
);

-- 插入 tables 数据
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (1, 1, '桌1 (女方)', 'round', 10, NULL, NULL, '女方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (2, 2, '桌2 (女方)', 'round', 10, NULL, NULL, '女方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (3, 3, '桌3 (女方)', 'round', 10, NULL, NULL, '女方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (4, 4, '桌4 (女方)', 'round', 10, NULL, NULL, '女方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (5, 5, '桌5 (女方)', 'round', 10, NULL, NULL, '女方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (6, 6, '桌6 (男方)', 'round', 10, NULL, NULL, '男方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (7, 7, '桌7 (男方)', 'round', 10, NULL, NULL, '男方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (8, 8, '桌8 (男方)', 'round', 10, NULL, NULL, '男方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (9, 9, '桌9 (男方)', 'round', 10, NULL, NULL, '男方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (10, 10, '桌10 (男方)', 'round', 10, NULL, NULL, '男方亲友区');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (11, 11, '桌11 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (12, 12, '桌12 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (13, 13, '桌13 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (14, 14, '桌14 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (15, 15, '桌15 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (16, 16, '桌16 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (17, 17, '桌17 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (18, 18, '桌18 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (19, 19, '桌19 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');
INSERT INTO tables (id, table_number, table_name, shape, capacity, x_coordinate, y_coordinate, notes) VALUES (20, 20, '桌20 (共同)', 'round', 10, NULL, NULL, '双方共同朋友/同事');

-- =========== 表: guest_tables ===========
CREATE TABLE IF NOT EXISTS guest_tables (
    id SERIAL PRIMARY KEY,
    guest_id INTEGER NOT NULL,
    table_id INTEGER NOT NULL,
    seat_number INTEGER,
    notes TEXT
);

-- 插入 guest_tables 数据
INSERT INTO guest_tables (id, guest_id, table_id, seat_number, notes) VALUES (1, 1, 1, 1, NULL);
INSERT INTO guest_tables (id, guest_id, table_id, seat_number, notes) VALUES (2, 2, 1, 2, NULL);

-- 脚本结束