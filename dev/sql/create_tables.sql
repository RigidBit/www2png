CREATE TABLE "api_keys"
(
	"id" serial NOT NULL,
	"api_key" char(36) NOT NULL,
	"user_id" INTEGER NOT NULL,
	"use_count" INTEGER NOT NULL DEFAULT 0,
	"timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX "ix_api_keys_api_key" ON "api_keys" ("api_key");

CREATE TABLE "data"
(
	"id" serial NOT NULL,
	"request_id" char(36) NOT NULL,
	"url" varchar(65535) NOT NULL,
	"block_id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	"queued" boolean NOT NULL,
	"pruned" boolean NOT NULL,
	"flagged" boolean NOT NULL,
	"removed" boolean NOT NULL,
	"failed" boolean NOT NULL,
	"timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

CREATE INDEX "ix_data_request_id" ON "data" ("request_id");
CREATE INDEX "ix_data_timestamp_pruned" ON "data" ("timestamp", "pruned");
CREATE INDEX "ix_data_url_user_id_queued" ON "data" ("url", "user_id", "queued");

CREATE TABLE "unverified_users"
(
	"id" serial NOT NULL,
	"email" varchar(255) NOT NULL,
	"challenge" char(36) NOT NULL,
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

INSERT INTO "users" (email, disabled) VALUES ('public@www2png.com', false);
