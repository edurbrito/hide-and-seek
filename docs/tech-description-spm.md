
Our Hide & Seek app was built following a generalized architectural pattern, with the system being divided into two big components, the backend and the frontend.
The backend service is composed of a REST API written in Python, served by the micro web framework Flask. This REST API is able to persist the data through a NoSQL MongoDB
database. The backend comunicates with the frontend by the HTTP web protocol, using the REST architectural pattern.
The frontend itself is represented by a Progressive Web App, written using the modern web tools, meaning, Javascript, HTML and CSS, with the help of the web framework Svelte
and Svelte Kit, and the CSS toolkit Tailwind.CSS. Being a PWA allows the Application to be delivered through the web, accessed through the devices' web browsers 
and run in any platform or operating system, with no major compatibility effort. It also allows to be installed and to behave similarly to a native phone App.
On the frontend, the OpenStreetMaps earth maps are used to display the user's current location, which is fetched using the device's Geolocation API.

The inner workings and the user flow of the app were inspired by other online multiplayer games, like Kahoot. In our case, for the sake of minimalizing the viability
of the product, we chose not the create a login mechanism, but rather rely on the mathematics of probability to authenticate, authorize and verify the integrity of the
users. Put in simple terms, each game session is identified by a randomly large token and it is the responsibility of the game creator to only allow trusted people to participate
in his/her game, by sharing the game code, or the game link, only with trusted people. The same mechanism was used with the users themselves, as each one is identified by a random authentication
token, which testifies their identity within the game. So, the app is cryptographically secure by the probabilities around the randomness of those tokens.
After that, it is all about joining a game with a valid code (that was previously created, i.e., it exists in the database), and play as a valid user.
The obvious cost of this flexibility is that anyone in the world can create a game and anyone in the world may join a game session, if he/she posesses the code.
For the sake of this MVP, there were no considerations made in this regard, however, it is pointed in the roadmap, to create mechanisms to prevent abusive use of the app.
