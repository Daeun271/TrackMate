# WebApp Client

A WebApp client for the sport data tracking API, intended for all users of the web browser and the application

Written using the Svelte 4 library.

## Development

### Prerequisites

-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

### Setup

1. Navigate to this directory:
    ```sh
    cd client
    ```
1. Install dependencies:
    ```sh
    npm install
    ```

### Run (Development)

```sh
npm run dev
```

This will run the client in development mode with hot reloading.
Note however that it runs independently from the host server, meaning that API requests will fail. You can start the server separately and then change the host address in the client to match the server's address. To do this modify the api host url in `./src/api.js`:

```js
let hostUrl = 'http://127.0.0.1:8000';
```

### Deployment

```sh
npm run build
```

This deploys the client to the API server's static file directory.
You can then start the server and navigate to the index of it to using your web browser use the client.
