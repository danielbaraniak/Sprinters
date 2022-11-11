<template>
  <body>
  <h1>HOUSE OF YOUR DREAMS</h1>
  <br>
  <br>
  <Map msg="Hi" @latitude="handleLatitude" @longitude="handleLongitude"/>
  <br>
  <div class="choose">
    <label class="text1" for="offer_type">Offer type:</label>
      <select v-model="posts.offer_type" name="offer_type" id="offer_type">
        <option value="" selected disabled hidden></option>
        <option value="Private">Private</option>
        <option value="Estate Agency">Estate Agency</option>
      </select>
    <br>
    <label class="text1" for="floors">Floor:</label>
      <select v-model.number="posts.floor" name="floors" id="floors">
        <option value="" selected disabled hidden></option>
        <option value="-1">-1</option>
        <option value="0">0</option>
        <option v-for="index in 10" :value="index" :key="index">{{index}}</option>
      </select>
    <br>
    <label class="text1" for="area">Area:</label>
      <input v-model.number="posts.area" type="number" id="area" name="area" min="10.00" step="0.01" oninput="validity.valid||(value='');">
    <br>
    <label class="text1" for="rooms">No of rooms:</label>
      <select v-model.number="posts.rooms" name="rooms" id="rooms">
        <option value="" selected disabled hidden></option>
        <option v-for="index in 4" :value="index" :key="index">{{index}}</option>
      </select>
    <br>
    <label class="text1" for="offer_type_of_building">Type of building:</label>
      <select v-model="posts.offer_type_of_building" name="offer_type_of_building" id="offer_type_of_building">
        <option value="" selected disabled hidden></option>
        <option value="Housing Block">Housing block</option>
        <option value="Tenement">Tenement</option>
        <option value="Apartment Building">Apartment building</option>
        <option value="Loft">Loft</option>
      </select>
    <br>
    <label class="text1" for="market">Market:</label>
      <select v-model="posts.market" name="market" id="market">
        <option value="" selected disabled hidden></option>
        <option value="Primary">Primary</option>
        <option value="Aftermarket">Aftermarket</option>
      </select>
    <br>
    <br>
  </div>
  <br>
  <br>
  <br>
  <br>
  <br>
  <br>
  <button class="button" role="button" v-on:click="postData">SEARCH</button>
</body>
</template>


<script>

import Map from './components/map.vue'

import Swal from 'sweetalert2'

import axios from 'axios'

export default {
  name: 'App',
  components: {
    Map
  },

  data(){
    return {
      posts:{
        offer_type:null,
        floor: null,
        area: null,
        rooms: null,
        market: null,
        offer_type_of_building: null,
        longitude: null,
        latitude: null
      }
    }
  },

  result() {
    return {
      price: null
    }
  },

  methods: {
    handleLatitude(value) {
      this.posts.latitude = value;
    },

    handleLongitude(value) {
      this.posts.longitude = value;
    },

    search1(price) {
      Swal.fire({
      title: price,
      width: 1000,
      padding: '3em',
      color: '#ffffff',
      background:  '#2e2e2e',
      confirmButtonColor: "#1beabd"
      })
    },

    postData() {

			let self = this;

			axios.post(`${process.env.VUE_APP_APIURL}/predict-price`, {
        'offer_type': self.posts.offer_type,
        'floor': self.posts.floor,
        'area': self.posts.area,
        'rooms': self.posts.rooms,
        'market': self.posts.market,
        'offer_type_of_building': self.posts.offer_type_of_building,
        "longitude": self.posts.longitude,
        "latitude": self.posts.latitude
      }).then(function (response) {
        self.search1(response.data.result.price);
			});
		},
  }
}
</script>

<style>
h1 {
  color: white;
}
.mapouter{
  position:relative;
  text-align:center;
  margin-left: auto;
  margin-right: auto;
  height:816px;
  width:825px;
}

.gmap_canvas{
  overflow:hidden;
  background:none!important;
  height:816px;
  width:825px;
}

.choose {
  display:flex; 
  flex-direction: row; 
  flex-wrap: wrap;
  justify-content: center; 
  align-items: center;
  gap: 10px;
  position: absolute;
  left: 50%;
  width: 1000px;
  padding: 40px;
  transform: translate(-50%, -50%);
  background-color: #262626;
  box-shadow: 0 15px 25px #1a1a1a;
  border-radius: 10px;
  max-width: 85%;
}

.text1 {
  color: white;
}

select {
  outline: none;
  padding: .3rem .3rem;
  border-radius: .5rem;
  color: #ffffff;
  padding-right: 3rem;
  font-family: Lato, sans-serif;
  font-weight: 500;
  font-size: 1rem;
  position: relative;
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;
  border: none;
  background: #313131 url("data:image/svg+xml;utf8,<svg viewBox='0 0 140 140' width='24' height='24' xmlns='http://www.w3.org/2000/svg'><g><path d='m121.3,34.6c-1.6-1.6-4.2-1.6-5.8,0l-51,51.1-51.1-51.1c-1.6-1.6-4.2-1.6-5.8,0-1.6,1.6-1.6,4.2 0,5.8l53.9,53.9c0.8,0.8 1.8,1.2 2.9,1.2 1,0 2.1-0.4 2.9-1.2l53.9-53.9c1.7-1.6 1.7-4.2 0.1-5.8z' fill='white' stroke='white' stroke-width='4'/></g></svg>") no-repeat;
  background-position: right .5rem top 50%;
}

input {
  outline: none;
  padding: .3rem .3rem;
  border-radius: .5rem;
  color: #ffffff;
  padding-right: 5rem;
  font-family: Lato, sans-serif;
  font-weight: 500;
  font-size: 1rem;
  position: relative;
  -moz-appearance: none;
  -webkit-appearance: none;
  appearance: none;
  border: none;
  background: #313131 no-repeat;
  background-position: right .5rem top 50%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  
}

/* CSS */
.button {

  padding: 1.2em 3em;
  border: none;
  outline: none;
  color: rgb(255, 255, 255);
  background: #111;
  cursor: pointer;
  position: relative;
  z-index: 0;
  border-radius: 20px;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

.button:before {
  content: "";
  background: linear-gradient(
    45deg,
    #ff0000,
    #ff7300,
    #fffb00,
    #48ff00,
    #00ffd5,
    #002bff,
    #7a00ff,
    #ff00c8,
    #ff0000
  );
  position: absolute;
  top: -2px;
  left: -2px;
  background-size: 400%;
  z-index: -1;
  filter: blur(5px);
  -webkit-filter: blur(5px);
  width: calc(100% + 5px);
  height: calc(100% + 5px);
  animation: glowing-button 20s linear infinite;
  transition: opacity 0.3s ease-in-out;
  border-radius: 10px;
}

@keyframes glowing-button {
  0% {
    background-position: 0 0;
  }
  50% {
    background-position: 400% 0;
  }
  100% {
    background-position: 0 0;
  }
}

.button:after {
  z-index: -1;
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background: #222;
  left: 0;
  top: 0;
  border-radius: 10px;
}

body {
  padding: 0;
  margin: 0;
  width: 100%;
  min-height: 100%; 
  background-color: #404040;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

</style>
