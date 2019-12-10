CREATE TABLE "api_keys"
(
	"id" serial NOT NULL,
	"uuid" char(36) NOT NULL,
	"user_id" INTEGER NOT NULL,
	"timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX "ix_data_uuid" ON "api_keys" ("uuid");

CREATE TABLE "data"
(
	"id" serial NOT NULL,
	"uuid" char(36) NOT NULL,
	"url" varchar(65535) NOT NULL,
	"block_id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"queued" boolean NOT NULL,
	"pruned" boolean NOT NULL,
	"flagged" boolean NOT NULL,
	"removed" boolean NOT NULL,
	"timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX "ix_data_uuid" ON "data" ("uuid");
CREATE INDEX "ix_data_timestamp_pruned" ON "data" ("timestamp", "pruned");

CREATE TABLE "unverified_users"
(
	"id" serial NOT NULL,
	"email" varchar(255) NOT NULL,
	"challenge" varchar(64) NOT NULL,
	"timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX "ix_unverified_users_challenge" ON "unverified_users" ("challenge");

CREATE TABLE "users"
(
	"id" serial NOT NULL,
	"email" varchar(255) UNIQUE NOT NULL,
	"disabled" boolean NOT NULL,
	"timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

ALTER TABLE "api_keys" ADD CONSTRAINT "fk_user_id" FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE "data" ADD CONSTRAINT "fk_user_id" FOREIGN KEY (user_id) REFERENCES users (id);

INSERT INTO "users" (email, disabled) VALUES ('tech@www2png.com', false);
