<template>
<div>
<h1>Roles ({{actor_detail.roles.length}})</h1>
<Loading :loading="loading"></Loading>
<table class="table table-bordered table-hover">
  <thead>
    <tr>
      <th>#</th>
      <th>Role</th>
      <th>Start Date</th>
      <th>End Date</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr   v-for="(actor_role,index) in actor_detail.roles" @click="selectProduct(actor_role)">
      <th>{{index+1}}</th>
      <th>{{actor_role.role_name}}</th>
      <th>{{actor_role.start_date}}</th>
      <th>{{actor_role.end_date}}</th>
        <button class="btn btn-danger" @click="deleteRole(actor_detail.actor_name,actor_role)"> X</button>
        <a class="btn btn-primary" v-bind:href="'/actors/' + actor_role.role_name"> &#9998; </a>
      
      </td>
    </tr>
  </tbody>
</table>

<div>


</div>
<div class = "info form">
  <form id="role_form">
      <div class="form group">
        <label for = "role_name">Role</label>
        <input v-model="actor_detail.roles.role_name" type="text" class="form-control" id="role_name" name = "role_name" aria-describedby="rolenameHelp" placeholder="Enter role">
        <small id="rolenameHelp" class="form-text text-muted">Enter actor's role</small>
      </div>
      <div class="form-group">
        <label for = "start_date">Start date</label>
        <input v-model="actor_detail.roles.start_date" type="text" class="form-control" id="start_date" aria-describedby="startdateHelp" placeholder="Enter start date">
        <small id="startdateHelp" class="form-text text-muted">Enter role's start date</small>
      </div>
      <div class="form-group">
        <label for = "end_date">End date</label>
        <input v-model="actor_detail.roles.end_date" type="text" class="form-control" id="end_date" aria-describedby="enddateHelp" placeholder="Enter end date.">
        <small id="enddateHelp" class="form-text text-muted">Enter role's end date. Must be greater than start date.</small>
      </div>
  <a class="btn btn-primary" @click="createRole()">Add</a>
  </form>

<h1>Synonyms ({{actor_detail.synonyms.length}})</h1>
<Loading :loading="loading"></Loading>
<table class="table table-bordered table-hover">
  <thead>
    <tr>
      <th>#</th>
      <th>synonym</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr   v-for="(actor_synonym,index) in actor_detail.synonyms" @click="selectProduct(actor_synonym)">
      <th>{{index+1}}</th>
      <th>{{actor_synonym.synonym}}</th>
        <button class="btn btn-danger" @click="deleteSynonym(actor_detail.actor_name,actor_synonym)"> X</button>
        <a class="btn btn-primary" v-bind:href="'/actors/' + actor_synonym.synonym"> &#9998; </a>
      
      </td>
    </tr>
  </tbody>
</table>
<div class = "info form">
  <form id="synonym_form">
      <div class="form group">
        <label for = "synonym">Synonym</label>
        <input v-model="actor_detail.synonyms.synonym" type="text" class="form-control" id="synonym" name = "synonym" aria-describedby="synonymHelp" placeholder="Enter synonym">
        <small id="synonymHelp" class="form-text text-muted">Enter a synonym for the actor</small>
      </div>
  <a class="btn btn-primary" @click="createSynonym()">Add</a>
  </form>
</div>

<h1>Reference links ({{actor_detail.wikis.length}})</h1>
<Loading :loading="loading"></Loading>
<table class="table table-bordered table-hover">
  <thead>
    <tr>
      <th>#</th>
      <th>Link</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr   v-for="(actor_wikilink,index) in actor_detail.wikis" @click="selectProduct(actor_wikilink)">
      <th>{{index+1}}</th>
      <th><a v-bind:href="actor_wikilink.wikilink">{{actor_wikilink.wikilink}}</a></th>
        <button class="btn btn-danger" @click="deleteWikilink(actor_detail.actor_name,actor_wikilink)"> X</button>
        <a class="btn btn-primary" v-bind:href="'/actors/' + actor_wikilink.wikilink"> &#9998; </a>
      
      </td>
    </tr>
  </tbody>
</table>
<div class = "info form">
  <form id="wikilink_form">
      <div class="form group">
        <label for = "wikilink">Reference link</label>
        <input v-model="actor_detail.wikis.wikilink" type="text" class="form-control" id="wikilink" name = "wikilink" aria-describedby="wikilinkHelp" placeholder="Enter link">
        <small id="wikilinkHelp" class="form-text text-muted">Enter a link to a webpage about the actor</small>
      </div>
  <a class="btn btn-primary" @click="createWikilink()">Add</a>
  </form>
</div>
</div>
</div>
</template>

<script>
/* eslint-disable */
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

import {APIService} from '../http/APIService';
import Loading from './Loading';
const API_URL = 'http://localhost:8000';
const apiService = new APIService();

export default {
  name: 'ActorList',
  components: {
    Loading
  },
  data() {
    return {
      selectedProduct:null,
      actor_detail: [],
      products: [],
      numberOfPages:0,
      pages : [],
      numberOfProducts:0,
      loading: false,
      nextPageURL:'',
      previousPageURL:''
    };
  }, 
  methods: {
    getProduct(){
      //this.loading = true;
      var current_actor = this.$route.params.actor_name;
      apiService.getProduct(current_actor).then((data) => {
        this.actor_detail = data;
        console.log(this.actor_detail.wikis);
        /*console.log(page);
        console.log(page.nextlink);
        this.numberOfProducts = page.count;
        this.numberOfPages = page.numpages;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        if(this.numberOfPages)
        {
          for(var i = 1 ; i <= this.numberOfPages ; i++)
          {
            const link = `/api/products/?page=${i}`;
            this.pages.push({pageNumber: i , link: link})
          }
        }*/
        this.loading = false;
      },
      function(data){
        //this.products = data;
        console.log(data);
      });
    },
    getPage(link){
      this.loading = true;  
      apiService.getProductsByURL(link).then((page) => {
        this.products = page.data;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        this.loading = false;
      });     
    },
    getNextPage(){
      console.log('next' + this.nextPageURL);
      this.loading = true;  
      apiService.getProductsByURL(this.nextPageURL).then((page) => {
        this.products = page.data;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        this.loading = false;
      });      
      
    },
    getPreviousPage(){
      this.loading = true;  
      apiService.getProductsByURL(this.previousPageURL).then((page) => {
        this.products = page.data;
        this.nextPageURL = page.nextlink;
        this.previousPageURL = page.prevlink;
        this.loading = false;
      });      
            
    },
    createRole(){
      var actor = this.$route.params.actor_name;
      var role = {
        role_name: document.getElementById('role_name').value,
        start_date: document.getElementById('start_date').value,
        end_date: document.getElementById('end_date').value
      };
      console.log('create product' + JSON.stringify(role));
      this.creating = true;
      apiService.createRole(actor,role).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 201)
        {
          alert("Role added");
          this.$router.go()
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    createSynonym(){
      var actor = this.$route.params.actor_name;
      var synonym_value = document.getElementById('synonym').value;
      var synonym = {
        synonym: synonym_value,
      };
      console.log('create product' + JSON.stringify(synonym));
      this.creating = true;
      apiService.createSynonym(actor,synonym).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 201)
        {
          alert("Synonym added");
          this.$router.go()
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    createWikilink(){
      var actor = this.$route.params.actor_name;
      var wikilink_value = document.getElementById('wikilink').value;
      var wikilink = {
        wikilink: wikilink_value,
      };
      console.log('create wikilink' + JSON.stringify(wikilink));
      this.creating = true;
      apiService.createWikilink(actor,wikilink).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 201)
        {
          alert("Reference link added");
          this.$router.go()
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    deleteRole(actor,role){
      console.log("deleting product: " + JSON.stringify(role))
      apiService.deleteRole(actor,role).then((r)=>{
        console.log(r);
        if(r.status === 204)
        {
          alert("Role deleted");
          this.$router.go()
          
        }
      })
    },
    deleteSynonym(actor,synonym){
      console.log("deleting product: " + JSON.stringify(synonym))
      apiService.deleteSynonym(actor,synonym).then((r)=>{
        console.log(r);
        if(r.status === 204)
        {
          alert("Synonym deleted");
          this.$router.go()
          
        }
      })
    },
    deleteWikilink(actor,wikilink){
      console.log("deleting wikilink: " + JSON.stringify(synonym))
      apiService.deleteWikilink(actor,wikilink).then((r)=>{
        console.log(r);
        if(r.status === 204)
        {
          alert("Wikilink deleted");
          this.$router.go()
          
        }
      })
    },
    selectProduct(product){
      this.selectedProduct = product;
    }
  },
  mounted() {
   
    this.getProduct();

  },
}
</script>
<style scoped>
.list-horizontal li {
	display:inline;
}
.list-horizontal li:before {
	content: '\00a0\2022\00a0\00a0';
	color:#999;
	color:rgba(0,0,0,0.5);
	font-size:11px;
}
.list-horizontal li:first-child:before {
	content: '';
}
</style>
