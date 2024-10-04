# modal-crdts

[CRDTs (Conflict-free Replicated Data Types)](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) are really useful data structures. CRDTs are often used in certain distributed systems to propagate changes across databases and file systems shared by multiple participants.

This example shows how you can leverage CRDTs via Yjs and websockets on [Modal](https://modal.com) to make a multiplayer text editing application.

> [!WARNING]
> This is meant for demo and learning purposes. Do not use this in production as is. CRDTs in production and at scale operate better with a primary caching layer and a secondary storage layer. You could use redis or valkey for caching and sql, object, or file storage for the secondary layer.

This example uses:

- FastAPI to host the web service
- Sqlite for storing document updates
- Ypy and Ypy-websocket for handling server side CRDT updates
- Yjs for client side awareness, editing, and rendering
- Quill for the editor
- ...and it all runs on [Modal](https://modal.com)

You'll notice that `app/static` has some javascript in it. That code is built from the code you'll find in the `web` directory.

Running `bun run build` from the `web` directory creates the client side js that's loaded by the html page.

To deploy this to modal and try it out for yourself, clone this repository and run `bin/deploy-modal`.

So where do we go from here? Maybe...

- Plugging in AI APIs as players that serve content through websockets
- Serving more than one room (right now this application only serves one room, `quill-demo`)
