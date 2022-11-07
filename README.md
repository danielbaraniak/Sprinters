# Sprinters
Competance project

## API Reference

#### Get predicted price

```http
  POST /predict-price
```
Limits
```
  One can send 1 request for every 5 seconds.
```

| Parameter | Type     | Is required| Restrictions  |
| :-------- | :------- | :--------- | :----------- |
| `offer_type` | `string` | ✅| X |
| `floor` | `float` | ✅  | In range from -1 to 11 |
| `area` | `float` | ✅  | Minimum value is 10.00 |
| `rooms` | `integer` | ✅| Minimum value is 1 |
| `offer_type_of_building` | `string` | ✅| X |
| `market` | `string` | ✅| X |
| `longitude` | `float` | ✅| X |
| `latitude` | `float` | ✅| X |

#### Example request

```http
{
  "offer_type":"Private",
  "floor":1.00,
  "area":57.0,
  "rooms":4,
  "market":"aftermarket",
  "offer_type_of_building":"Housing Block",
  "longitude": 19.742433230687826,
  "latitude": 51.805085715344035
}
```
