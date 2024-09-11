# bhajibackend
The Backend for Bhajiwala Partner and Consumer

## API:

### Cart Ops
- `PUT /cart/<partner_id>` : add vegetable item to the partner's cart

    `BODY: {"vegetableId": <vegetableId>, "price": <price>}`

- `DELETE /cart/<partner_id>` : remove vegetable item from the partner's cart

    `BODY: {"vegetableId": <vegetableId>}`

- `POST /cart/<partner_id>`: add all items at once (to reduce api calls)

    `BODY: {"items":[{"vegetableId":<vegetableId>, "price": <price>}]}`

- `GET /cart/<partner_id>`: list all items in the cart along with their price
