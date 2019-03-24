# asyncio-pg-nats-bridge [In Progress]
Example bridge between postgres and nats message queue.

## Planned Functionality (minimal)
* A service will LISTEN to a defined postgres channel.
* A sample table will be created in Postgres with an attached trigger.
* An ON UPDATE trigger will issue a NOTIFY for the defined channel showing the updated values.
* The bridging service will receive the notify and publish the notify onto a receiving NATS message queue.
* A wiretap will listen to the queue and emit the notify message to the display.

## Future
* Use PipelineDb (https://www.pipelinedb.com/) or plug in to enable streaming continuuos queries / aggregates to be used to generate a CEP stream into NATS.

## To demonstrate
1. Run docker image.
2. Run postgres image and initialise database.
3. Run the wiretap to emit received notification messages.
4. Run the simulator to generate test messages.

## References
* https://tapoueh.org/blog/2018/07/postgresql-listen/notify/




