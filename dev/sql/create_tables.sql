CREATE TABLE "data"
(
  "id" serial NOT NULL,
  "uuid" char(36) NOT NULL,
  "url" varchar(65535) NOT NULL,
  "block_id" INTEGER NOT NULL,
  "user_id" INTEGER NOT NULL,
  "flagged" boolean NOT NULL,
  "removed" boolean NOT NULL,
  "pruned" boolean NOT NULL,
  "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX "ix_data_uuid" ON "data" ("uuid");
CREATE INDEX "ix_data_timestamp_pruned" ON "data" ("timestamp", "pruned");

CREATE TABLE "users"
(
  "id" serial NOT NULL,
  "email" varchar(255) UNIQUE NOT NULL,
  "password" varchar(255) NOT NULL,
  "disabled" boolean NOT NULL,
  "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE "unverified_users"
(
  "id" serial NOT NULL,
  "email" varchar(255) NOT NULL,
  "challenge" char(64) NOT NULL,
  "timestamp" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (id)
);

CREATE INDEX "ix_unverified_users_challenge" ON "unverified_users" ("challenge");

ALTER TABLE "data" ADD CONSTRAINT "fk_user_id" FOREIGN KEY (user_id) REFERENCES users (id);
