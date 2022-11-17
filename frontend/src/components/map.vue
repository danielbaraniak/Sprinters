<template>
  <div class="wrap">
      <div class="location">
          <p>Choose location:</p>
      </div>
      <br>
      <br>
      <br>
      <div id="map"></div>
  <br>
  <br>
  <form action="" class="form">
      <input type="text" id="latitude" placeholder="latitude" :value="latitude" @input='$emit("latitude", $event.target.value)' />
      <input type="text" id="longitude" placeholder="longitude" :value="longitude" @input='$emit("longitude", $event.target.value)' />
  </form>
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>
</div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";

export default {
name: "LeafletMap",
data() {
return {
map: null,
latitude: null,
longitude: null
};
},

emits: ['latitude', 'longitude'],

props: {
msg: String
},

watch: {
latitude() {
this.$emit("latitude", this.latitude);
},

longitude() {
this.$emit("longitude", this.longitude);
}
},

mounted() {
let recaptchaScript = document.createElement('script')
recaptchaScript.setAttribute('src', 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.js')
document.head.appendChild(recaptchaScript)

let mapOptions = {
center:[52.224, 21.025],
zoom:10,
}

let map = new L.map('map' , mapOptions);

let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
map.addLayer(layer);

let self = this;
let marker = null;

map.on('click', (event)=> {

if(marker !== null){
    map.removeLayer(marker);
}

marker = L.marker([event.latlng.lat , event.latlng.lng]).addTo(map);

self.latitude = event.latlng.lat;
self.longitude = event.latlng.lng;
})
}
};
</script>

<style scoped>
@import 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css';
#map {
width: 50vw;
height: 50vh;
display: block;
margin-left: auto;
margin-right: auto;
outline-style: groove;
}

.form {
display:flex; 
flex-direction: row; 
justify-content: center; 
align-items: center;
gap: 10px;
position: absolute;
left: 50%;
width: 1000px;
padding-left: 40px;
padding-right: 40px;
padding-top: 10px;
padding-bottom: 10px;
transform: translate(-50%, -50%);
background-color: #262626;
box-shadow: 0 15px 25px #1a1a1a;
border-radius: 10px;
max-width: 85%;
}

.location {
color: white;
display:flex; 
flex-direction: row; 
justify-content: center; 
align-items: center;
gap: 10px;
position: absolute;
left: 50%;
width: 1000px;
padding-left: 40px;
padding-right: 40px;
padding-top: 1px;
padding-bottom: 1px;
transform: translate(-50%, -50%);
background-color: #262626;
box-shadow: 0 15px 25px #1a1a1a;
border-radius: 10px;
font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
max-width: 85%;
}

input {
outline: none;
padding: .3rem .3rem;
border-radius: .5rem;
color: #ffffff;
padding-right: 0.9rem;
font-family: Lato, sans-serif;
font-weight: 500;
font-size: 1rem;
position: relative;
-moz-appearance: none;
-webkit-appearance: none;
appearance: none;
border: none;
background: #313131;
background-position: right .5rem top 50%;
font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

</style>