# asyncio-pg-nats-bridge [In Progress]
Example bridge between postgres and nats message queue.

![](./images/context.jpg)

## Planned Functionality (minimal)
* A service will LISTEN to a defined postgres channel.
* A sample table will be created in Postgres with an attached trigger.
* An ON UPDATE trigger will issue a NOTIFY for the defined channel showing the updated values.
* The bridging service will receive the notify and publish the notify onto a receiving NATS message queue.
* A wiretap will listen to the queue and emit the notify message to the display.

## Future
* Use PipelineDb (https://www.pipelinedb.com/) or plug in to enable streaming continuuos queries / aggregates to be used to generate a CEP stream into NATS.

## To demonstrate
1. Run NATS docker image.
2. Run Postgres docker image and initialise database.
3. Run the wiretap to emit received notification messages.
4. Run the simulator to generate test messages.

## References
* https://tapoueh.org/blog/2018/07/postgresql-listen/notify/
* https://magicstack.github.io/asyncpg/current/api/index.html?highlight=listen#asyncpg.connection.Connection.add_listener

## Notes
``` bash
# Running the NATS docker image
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name gnatsd -ti nats:latest

#### Running the Postgres docker image
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=password -d postgres

#### To access docker pgdb using local psql
psql -h localhost -U postgres

#### To access psql through running docker image
docker exec -it postgres psql -U postgres

```

``` sql
#### Database setup
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE TABLE fixtures (fixture_id uuid primary key, params json not null);
DROP TABLE fixtures;
CREATE TABLE fixtures (fixture_id int primary key, params int not null);


#### Create trigger with Notify on Create, Update or Delete
begin;

create or replace function tg_notify ()
 returns trigger
 language plpgsql
as $$
declare
  channel text := TG_ARGV[0];
begin
  PERFORM (
     with payload(key, params) as
     (
       select NEW.fixture_id, NEW.params as fixs
     )
     select pg_notify(channel, row_to_json(payload)::text)
       from payload
  );
  RETURN NULL;
end;
$$;

CREATE TRIGGER notify_fixtures
         AFTER INSERT
            ON fixtures
      FOR EACH ROW
       EXECUTE PROCEDURE tg_notify('fixtures.parameters');

commit;

-- To setup listeners to Async notify channel.
LISTEN fixtures.parameters;

-- Inserting a dummy record to test async notifications.
insert into fixtures values (4,1);
```

## Dependencies
```bash
pip install --upgrade pip
pip install asyncio
pip install asyncpg
pip install asyncio-nats-client
```

