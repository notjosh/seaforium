ALTER TABLE threads MODIFY threads.subject VARCHAR(96) CHARACTER SET utf8 NOT NULL;
ALTER TABLE pm_content MODIFY pm_content.subject VARCHAR(96);
ALTER TABLE titles MODIFY titles.title_text VARCHAR(36) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL;