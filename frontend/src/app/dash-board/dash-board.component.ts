import { Component, ViewContainerRef, ViewEncapsulation,ViewChild,TemplateRef,OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpModule } from '@angular/http';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';
import { DashBoardService } from './dash-board.service';
import * as moment from 'moment';
import * as _ from 'lodash';
import { overlayConfigFactory } from 'angular2-modal';
import { Overlay } from 'angular2-modal';

import {
  VEXBuiltInThemes,
  Modal,
  DialogPreset,
  DialogFormModal,
  DialogPresetBuilder,
  VEXModalContext,
  VexModalModule,
  providers
} from 'angular2-modal/plugins/vex';

@Component({
  selector: 'dash-board',
  templateUrl: './dash-board.component.html',
  styleUrls: [
    './dash-board.component.css'
  ],
})

export class DashBoardComponent implements OnInit {
  constructor(
    private router: Router,
    private _fb: FormBuilder,
    public modal: Modal,
    private dashBoardService: DashBoardService,
    private agendaService: AgendaService
  ){}

  agendas = this.dashBoardService.agendas;
  user = this.dashBoardService.currentUser;
  @ViewChild('templateRef') public templateRef: TemplateRef<any>;
  @ViewChild('signUpSuccessRef') public signUpSuccessRef: TemplateRef<any>;

  //feedback for input
  loginEmailError: string;
  loginPasswordError: string;
  registerEmailError: string;
  registerPasswordError: string;
  formErrors = { name:"",start:"",duration:"",website:"",other:""};
  today = moment().add(1, 'day').format("YYYY-MM-DD");
  addNewAgenda = false;
  deleting = false;
  deletedAgenda: Agenda;
  //hide = false;

  loginEmail: string;
  loginPassword: string;
  //for testing
  // loginEmail = 'meganmckenzie@gmail.com';
  // loginPassword = '^Z2AwhuJ)T';
  registerEmail: string;
  registerPassword: string;
  organiser: string;
  event: string;
  signingUp = false;
  
  agendaLoading = false;
  newAgendaSubmitting = false;
  loginSubmitting = false;
  registerSubmitting = false;

  agendaForm: FormGroup;

  ngOnInit() {
    if (this.user.authed) {
      this.getAgendas();
    }
    
    this.agendaForm = this._fb.group({
      //validators currently not in use
      name: ['', [<any>Validators.required]],
      description: [''],
      location: [''],
      start: ['', [<any>Validators.required]],
      duration: [3, [Validators.required,Validators.pattern('^[1-9]$')]],
      website:'',
      tracks: [[]],
    });
  }

  clearLoginErrors(){
    this.loginEmailError=undefined;
    this.loginPasswordError=undefined;
  }

  clearSignUpErrors(){
    this.registerEmailError=undefined;
    this.registerPasswordError=undefined;
  }

  signUp() {
    if (!this.registerEmail || !this.registerPassword) { 
      if(!this.registerEmail){
        this.registerEmailError = "Please enter email";
      }
      if(!this.registerPassword){
        this.registerPasswordError = "Please enter password";
      }
      return;
    }
    this.registerSubmitting = true;
    this.dashBoardService.signUp(this.registerEmail, this.registerPassword,this.organiser,this.event).subscribe(
      status => { 
        this.registerSubmitting = false;
        if (status === 201){ 
          this.modal.open(this.signUpSuccessRef, overlayConfigFactory({ isBlocking: false }, VEXModalContext));
          this.toggleSigningUp();
        }
      },
      error =>  {
        this.registerSubmitting = false;
        if(error.username){
          this.registerEmailError = error.username[0];
        }
        if(error.password){
          this.registerPasswordError = error.password[0];
        }
        if(error.non_field_errors){
          this.registerPasswordError = error.non_field_errors[0];
        }      
      }
    );
  }

  logIn() {
    if (!this.loginEmail || !this.loginPassword) { 
      if(!this.loginEmail){
        this.loginEmailError = "Please enter email";
      }
      if(!this.loginPassword){
        this.loginPasswordError = "Please enter password";
      }
      return;
    }
    this.loginSubmitting = true;
    this.dashBoardService.logIn(this.loginEmail, this.loginPassword).subscribe(
      success => { 
        this.loginSubmitting = false;
        this.getAgendas();
      },
      error => {
        this.loginSubmitting = false;
        if(error.username){
          this.loginEmailError = error.username[0];
        }
        if(error.password){
          this.loginPasswordError = error.password[0];
        }
        if(error.non_field_errors){
          this.loginPasswordError = error.non_field_errors[0];
        }
      }
    );
  }

  getAgendas() {
    this.agendaLoading = true;
    this.dashBoardService.getAgendas().subscribe(
      (data: Agenda[]) => {
        this.agendaLoading = false;
        this.agendas = _.sortBy(data, agenda => -agenda.id);
      },
      error => {
       console.log(error);
      }
    );
  }

  submitAgendaForm() {
    if(this.checkAgendaForm()){
      this.createAgenda();
    }
  }

  checkAgendaForm():boolean{
    let isValid = true;
    if(!this.agendaForm.value.name || this.agendaForm.value.name.trim() === '' ){
      this.formErrors.name = 'Required';
      isValid = false;
    }
    if(!this.agendaForm.value.start){
      this.formErrors.start = 'Required';
      isValid = false;
    }
    if(!this.agendaForm.value.duration){
      this.formErrors.duration = 'Required';
      isValid = false;
    }
    if(this.agendaForm.value.duration && (this.agendaForm.value.duration < 1 || this.agendaForm.value.duration > 9)){
      this.formErrors.duration = 'Duration must be between 1 and 9 days';
      isValid = false;
    }
    return isValid;
  }

  createAgenda() {
    this.newAgendaSubmitting = true;
    // Add URL schema if not included
    let website = this.agendaForm.value.website;
    if (website && !website.match(/^https?:\/\//i)) {
      website = 'http://' + website;
    }
    
    this.dashBoardService.createAgenda(
      this.agendaForm.value.name, 
      this.agendaForm.value.description, 
      this.agendaForm.value.location, 
      this.agendaForm.value.start, 
      this.agendaForm.value.duration,
      website,
      this.agendaForm.value.tracks
    ).subscribe(
      data => { 
        this.addNewAgenda = true;
        this.agendas.unshift(data);
        this.newAgendaSubmitting = false;
        this.agendaForm.reset({
            name: '',
            description: '',
            location: '',
            start: '',
            duration: 3,
            website:'',
            tracks: [],
        });
      },
      error => {
        this.newAgendaSubmitting = false;
        console.log(error);
        
        // Map the fields returned by the server to the fields used 
        // on the client side
        const fields = {
          name: 'name', 
          start_at: 'start',
          duration: 'duration',
          website: 'website',
          non_field_errors: 'other',
        };
        
        _.forEach(fields, (formField, serverField) => {
          if (error[serverField]) {
            this.formErrors[formField] = error[serverField].join(' ');
          }
        });
      }
    );
  }

  deleteAgendaCheck(agenda: Agenda) {
    this.deletedAgenda = agenda;
    if (agenda.published) {
      this.modal.open(this.templateRef, overlayConfigFactory({ isBlocking: true }, VEXModalContext));
    } else {
      this.deleteAgenda(agenda);
    }   
  }
  
  callDeleteAgenda(evt: any, agenda: Agenda) {
    evt.stopPropagation();
    this.deleteAgendaCheck(agenda);
  }

  deleteAgenda(agenda: Agenda, dialog?:any) {
    this.dashBoardService.deleteAgenda(agenda.id).subscribe(
      () => {
        this.addNewAgenda = false;
        _.remove(this.agendas, agenda);
      },
      error => {
        console.log(error);
      }
    );
    
    if (dialog){
      dialog.close(true);
    }
  }
  
  trackByAgendaId (index: number, agenda: Agenda) {
    return agenda.id;
  }

  onSelect(agenda: Agenda) {
    this.router.navigate(['/agenda', agenda.id]);
  }

  toggleSigningUp() {
    this.signingUp = !this.signingUp;
  }
  
  clearError(field: string = '') {
    if (field.length) {
      delete this.formErrors[field];
    }
    delete this.formErrors.other;
  }
}
