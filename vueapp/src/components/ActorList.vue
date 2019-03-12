<template>
<div>
  <div class="col-sm-5" style="max-width:30%;width:15%;">
    <h1>Actors ({{actors.data.length}})</h1>
    <Loading :loading="loading"></Loading>
    <div class = "info form" style="max-width:150px;width:150px;margin-right:0px;padding-right=0px;">
      <form id="actor_form">
          <div class="form group">
            <input v-model="actors.actor_name" type="text" class="form-control" id="actor" name = "actor" aria-describedby="actorHelp" placeholder="Enter actor" maxlength="150">
            <small id="actorHelp" class="form-text text-muted">Enter actor's name</small>
          </div>
      <a class="btn btn-primary" @click="createActor()">Add</a>
      </form>
    </div>
    <div class="filters">

      <!-- <div class="filter">
        <label for="component-dropdown">Select Actor: </label>
        <dropdown id="component-dropdown" :options="actor_list" v-model="selectedActor"></dropdown>
      </div> -->
      <!-- <div>
        <tr v-for="(actor,index) in actor_list">
          <th v-model="selectedActor" @click="getActorDetail()">{{actor}}</th>
        </tr>
      </div> -->
      <div style="overflow: auto; height: 200px;width:150%">
        <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>Actor</th>
          </tr>
        </thead>
        <tbody id="actor_table">
          <tr   v-for="(actor) in actor_list" @click="selectActor(actor)">
            <th>{{actor}}</th>
          </tr>
        </tbody>
      </table>
    </div>
      <!-- <a class="btn btn-primary" @click="getActorDetail()">Select</a> -->
      <div class="result">
        Selected: <strong>{{ selectedActor }}</strong>
      </div>
      <button class="btn btn-danger" @click="deleteSelectedActor()"> Delete</button>
      <button class="btn btn-danger" @click="lockSelectedActor()"> Lock</button>
      <small id="lockHelp" class="form-text text-muted">Lock actor once all updates are done.</small>
    </div>
  </div>

  <div class="col-sm-5" style="max-width:30%;width:23%;">
    <h1>Reference links ({{actor_detail.wikis.length}})</h1>
    <Loading :loading="loading"></Loading>
    <table class="table table-bordered table-hover table-editable">
      <thead>
        <tr>
          <th>#</th>
          <th>Link</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr   v-for="(actor_wikilink,index) in actor_detail.wikis">
          <th>{{index+1}}</th>
          <th style="word-break: break-all;"><a v-bind:href="actor_wikilink.wikilink">{{actor_wikilink.wikilink}}</a></th>
            <button class="btn btn-danger" @click="deleteWikilink(actor_detail.actor_name,actor_wikilink)"> X</button>
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

  <div class="col-sm-5">
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
      <tbody id="role_table">
        <tr   v-for="(actor_role,index) in actor_detail.roles">
          <th>{{index+1}}</th>
          <th v-model="actor_role.role_name" id="edit_role_name" name="edit_role_name">{{actor_role.role_name}}</th>
          <th contenteditable>{{actor_role.start_date}}</th>
          <th contenteditable>{{actor_role.end_date}}</th>
          <button class="btn btn-danger" @click="deleteRole(actor_detail.actor_name,actor_role)"> X</button>
          <a class="btn btn-primary" @click="updateRole(index)"> &#9998; </a>
        </tr>
      </tbody>
    </table>
    <div v-for="err in error" v-if="showError" class="alert alert-danger">
        {{err}}
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
            <small id="startdateHelp" class="form-text text-muted">Enter role's start date.</small>
          </div>
          <div class="form-group">
            <label for = "end_date">End date</label>
            <input v-model="actor_detail.roles.end_date" type="text" class="form-control" id="end_date" aria-describedby="enddateHelp" placeholder="Enter end date">
            <small id="enddateHelp" class="form-text text-muted">Enter role's end date. Must be greater than start date.</small>
          </div>
      <a class="btn btn-primary" @click="createRole()">Add</a>
      </form>
    </div>
  </div>

  <div class="col-sm-5" style="inline-block;float:right;">
    <h1>Synonyms ({{actor_detail.synonyms.length}})</h1>
    <Loading :loading="loading"></Loading>
    <table class="table table-bordered table-hover">
      <thead>
        <tr>
          <th>#</th>
          <th>Synonym</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr   v-for="(actor_synonym,index) in actor_detail.synonyms">
          <th>{{index+1}}</th>
          <th>{{actor_synonym.synonym}}</th>
            <button class="btn btn-danger" @click="deleteSynonym(actor_detail.actor_name,actor_synonym)"> X</button>          
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
import Dropdown from '@/components/Dropdown'
const API_URL = 'http://localhost:8000';
const apiService = new APIService();

export default {
  name: 'ActorList',
  components: {
    Loading,
    'dropdown': Dropdown
  },
  data() {
    return {
      error: [],
      selectedProduct:null,
      selectedActor: null,
      selectedOption: null,
      showError:false,
      initialActor: '',
      products: [],
      actor_list:{},
      actors: [],
      actor_detail: [],
      numberOfPages:0,
      pages : [],
      numberOfProducts:0,
      loading: false,
      nextPageURL:'',
      previousPageURL:''
    };
  }, 
  methods: {
    getActors(){
      //this.loading = true;
      apiService.getActors().then((data) => {
        this.actors = data;
        this.showError=false;
        //console.log(this.actors.actor_detail);
        for(var key in this.actors){
            var value = this.actors[key];
            if(Object.keys(value).length==0){
              console.log(value)
              break;
            }
            for(var key2 in value){
              if(this.selectedActor==null) this.selectedActor = String(value[key2].actor_name);
              this.getActorDetail();
              this.selectedOption = this.value;
              this.actor_list[value[key2].actor_name]=value[key2].actor_name;
            }
        }
        this.loading = false;
      },(error)=>{
        this.error=[];
        this.showError=true;
        for(var key in error.response.data){
          this.error.push(error.response.data[key][i]);
        }
      });
    },
    getActorDetail(){
      //this.loading = true;
      this.showError=false;
      var current_actor = this.selectedActor;
      apiService.getActor(current_actor).then((data) => {
        this.actor_detail = data;
        for(var key in this.actor_detail.wikis){
          this.actor_detail.wikis[key].wikilink=this.actor_detail.wikis[key].wikilink.replace(/\*/g,'/')
        }
        this.loading = false;
      },(error)=>{
        this.error=[];
        this.showError=true;
        for(var key in error.response.data){
          for(var i=0;i<error.response.data[key].length;i++){
            this.error.push(error.response.data[key][i]);
          }
        }
      });
    },
    createActor(){
      var actor = document.getElementById('actor').value;
      console.log('create actor' + JSON.stringify(actor));
      this.creating = true;
      apiService.createActor(actor).then((result)=>{
          this.showError=false;
          console.log(result);
          // success 
          if(result.status === 201)
        {
          alert("Actor added");
          this.$router.go()
        }
            sleep(1000).then(() => {
               this.creating = false;
            })
      },(error)=>{
        this.error=[];
        this.showError=true;
        for(var key in error.response.data){
          for(var i=0;i<error.response.data[key].length;i++){
            this.error.push(error.response.data[key][i]);
          }
        }
      });
    },

    createRole(){
      var actor = this.selectedActor;
      var role = {
        role_name: document.getElementById('role_name').value,
        start_date: document.getElementById('start_date').value,
        end_date: document.getElementById('end_date').value
      };
      console.log(role);
      this.creating = true;
      apiService.createRole(actor,role).then((result)=>{
          this.showError=false;
          console.log(result);
          // success 
          if(result.status === 201)
        {
          this.getActorDetail();
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.error=[]
        this.showError = true;
        for(var key in error.response.data){
          this.error.push(error.response.data[key]);
          // for(var i=0;i<error.response.data[key].length;i++){
          //   console.log(Array.isArray(error.response.data[key]));
          //   this.error.push(error.response.data[key][i]);
          // }
        }
      });
    },
    createSynonym(){
      var actor = this.selectedActor;
      var synonym_value = document.getElementById('synonym').value;
      var synonym = {
        synonym: synonym_value,
      };
      console.log('create product' + JSON.stringify(synonym));
      this.creating = true;
      apiService.createSynonym(actor,synonym).then((result)=>{
          // success
          this.showError=false
          if(result.status === 201)
        {
          this.getActorDetail();
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.error=[]
        this.showError=true
        for(var key in error.response.data){
          for(var i=0;i<error.response.data[key].length;i++){
            this.error.push(error.response.data[key][i]);
          }
        }
      });
    },
    createWikilink(){
      var actor = this.selectedActor;
      var wikilink_value = document.getElementById('wikilink').value;
      wikilink_value = wikilink_value.replace(/\//g,'*');
      var wikilink = {
        wikilink: wikilink_value,
      };
      console.log('create wikilink' + JSON.stringify(wikilink));
      this.creating = true;
      apiService.createWikilink(actor,wikilink).then((result)=>{
        this.showError=false
          // success 
          if(result.status === 201)
        {
          this.getActorDetail();
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        this.error=[]
        this.showError=true
        for(var key in error.response.data){
          for(var i=0;i<error.response.data[key].length;i++){
            this.error.push(error.response.data[key][i]);
          }
        }
      });
    },
    deleteSelectedActor(){
      var actor = this.selectedActor;
      apiService.deleteActor(actor).then((r)=>{
        if(r.status===204){
          alert("Actor "+actor+" deleted");
          this.$router.go()
        }
      })
    },
    deleteRole(actor,role){
      console.log("deleting product: " + JSON.stringify(role))
      apiService.deleteRole(actor,role).then((r)=>{
        console.log(r);
        if(r.status === 204)
        {
          this.getActorDetail();
          
        }
      })
    },
    deleteSynonym(actor,synonym){
      console.log("deleting product: " + JSON.stringify(synonym))
      apiService.deleteSynonym(actor,synonym).then((r)=>{
        if(r.status === 204)
        {
          this.getActorDetail();
          
        }
      })
    },
    deleteWikilink(actor,wikilink){
      wikilink.wikilink = wikilink.wikilink.replace(/\//g,'*')
      console.log(wikilink)
      console.log("deleting wikilink: " + JSON.stringify(synonym))
      apiService.deleteWikilink(actor,wikilink).then((r)=>{
        console.log(r);
        if(r.status === 204)
        {
          tthis.getActorDetail();
        }
      })
    },
    updateRole(index){
      var actor = this.selectedActor;
      console.log(document.getElementById('role_table').rows[index].cells[3].innerHTML);
      var role = {
        role_name : document.getElementById('role_table').rows[index].cells[1].innerHTML,
        start_date : document.getElementById('role_table').rows[index].cells[2].innerHTML,
        end_date : document.getElementById('role_table').rows[index].cells[3].innerHTML
      }
      console.log(role);
      this.creating = true;
      apiService.createRole(actor,role).then((result)=>{
          console.log(result);
          // success 
          if(result.status === 201)
        {
          this.getActorDetail();
        }
            sleep(1000).then(() => {
               this.creating = false;
            })          
      },(error)=>{
        console.log("role update error")
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    lockSelectedActor(){
      var actor = this.selectedActor;
      apiService.lockActor(actor).then((result)=>{
        if(result.status===200){
          alert("Actor "+this.selectedActor+" locked");
          this.$router.go();
        }
      },(error)=>{
        console.log("actor lock error")
        this.showError = true;
            sleep(1000).then(() => {
               this.creating = false;
            })
      });
    },
    selectActor(actor){
      this.selectedActor = actor;
      this.getActorDetail();
    },
    test(){
      console.log("this is a test");
    }
  },
  mounted() {
    this.getActors();
  },
  watch: {
  value: function (newValue) {
    this.selectedOption = newValue
  }
}
}
</script>
<style scoped>
.form-control{
  width: 150px;
  max-width: 150px;
}
.info form{
  max-width:150px;
}
.col-sm-5{
  display:inline-block;
  float:left;
  padding-right:0px;
  max-width:30%;
}
.table{
  width:80%;
}
.filters {
  width: 300px;
  margin: 10 auto;
  max-width:70%;
}

.filter {
  text-align: left;
}
.btn-danger{
  margin: 5px;
}
.result {
  margin-top: 10px;
  text-align: left;
}

label {
  display: block;
}
.list-horizontal li {
	display:inline-block;
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
