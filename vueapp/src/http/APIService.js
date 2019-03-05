/* eslint-disable */
import axios from 'axios';
import AuthService from '../auth/AuthService';
const API_URL = 'http://localhost:8000';

export class APIService{
    constructor(){
      
    }
    getAuthToken(){
        return axios.post(this.$store.state.endpoints.obtainJWT, payload);
    }
    getActors() {
        const url = `${API_URL}/actors/`;
        return axios.get(url).then(response => response.data);
    }
    getProductsByURL(link){
        const url = `${API_URL}${link}`;
        return axios.get(url).then(response => response.data);
        
    }
    getProduct(actor_name) {
        const url = `${API_URL}/actors/${actor_name}`;
        return axios.get(url).then(response => response.data);
    }    
    deleteRole(actor,role){
        const url = `${API_URL}/actors/${actor}/roles/${role.role_name}/${role.start_date}`;
        return axios.delete(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});

    }
    deleteSynonym(actor,synonym){
        const url = `${API_URL}/actors/${actor}/synonyms/${synonym.synonym}`;
        return axios.delete(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});

    }
    deleteWikilink(actor,wikilink){
        console.log(wikilink.wikilink);
        const url = `${API_URL}/actors/${actor}/wikis/${wikilink.wikilink}`;
        return axios.delete(url, { headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});

    }
    createRole(actor,role){
        const url = `${API_URL}/upload/`;
        var roles = [];
        var synonyms = [];
        var wikilinks = [];
        roles.push(role);
        var data = {
            actor_name : actor,
            roles : roles,
            synonyms : synonyms,
            wikis : wikilinks
        };
        console.log(data);
        const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
        return axios.post(url,data,{ headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});
    }
    createSynonym(actor,synonym){
        const url = `${API_URL}/upload/`;
        console.log(synonym);
        var roles = [];
        var synonyms = [];
        var wikilinks = [];
        synonyms.push(synonym);
        var data = {
            actor_name : actor,
            roles : roles,
            synonyms : synonyms,
            wikis : wikilinks
        };
        console.log(data);
        const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
        return axios.post(url,data,{ headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});
    }
    createWikilink(actor,wikilink){
        const url = `${API_URL}/upload/`;
        console.log("here?");
        console.log(wikilink);
        var roles = [];
        var synonyms = [];
        var wikilinks = [];
        wikilinks.push(wikilink);
        var data = {
            actor_name : actor,
            roles : roles,
            synonyms : synonyms,
            wikis : wikilinks
        };
        const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
        return axios.post(url,data,{ headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});
    }
    createActor(actor){
        const url = `${API_URL}/actors/`;
        var data = {
            actor_name: actor,
        }
        const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
        return axios.post(url,data,{ headers: { Authorization: `Bearer ${AuthService.getAuthToken()}` }});
    }
    updateProduct(product){
        const url = `${API_URL}/actors/${product}`;
        const headers = {Authorization: `Bearer ${AuthService.getAuthToken()}`};
        return axios.put(url,product,{headers: headers});
    } 
} 