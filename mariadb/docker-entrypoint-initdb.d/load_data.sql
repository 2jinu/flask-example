INSERT INTO roles (name) VALUES ('ADMIN'), ('USER');
INSERT INTO users (username, password) VALUES ('admin', 'scrypt:32768:8:1$cps213Dl9oKmyhZD$0769090c38309b39109aba6a6ef077a747b245bcf2411b5aae18fc5a986ac2ab04276ec38a8ac6f1eb478e2b92305496c529f70176aff220575243f43cead8a4');
INSERT INTO rel_user_roles (user_id, role_id) VALUES (1, 1);
INSERT INTO users (username, password) VALUES ('user1', 'scrypt:32768:8:1$cps213Dl9oKmyhZD$0769090c38309b39109aba6a6ef077a747b245bcf2411b5aae18fc5a986ac2ab04276ec38a8ac6f1eb478e2b92305496c529f70176aff220575243f43cead8a4');
INSERT INTO rel_user_roles (user_id, role_id) VALUES (2, 2);