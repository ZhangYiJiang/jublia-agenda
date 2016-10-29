import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpModule } from '@angular/http';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { Agenda } from '../agenda/agenda';
import { AgendaService } from '../agenda/agenda.service';
import { DashBoardService } from './dash-board.service';

@Component({
  selector: 'dash-board',
  templateUrl: './dash-board.component.html',
  styleUrls: ['./dash-board.component.css']
})

export class DashBoardComponent implements OnInit {
  constructor(
    private router: Router,
    private _fb: FormBuilder,
    private dashBoardService: DashBoardService,
    private agendaService: AgendaService
  ){}

  agendas = this.dashBoardService.agendas;
  user = this.dashBoardService.currentUser;

  //successMsg: string;

  //feedback for input
  loginEmailError: string;
  loginPasswordError: string;
  registerEmailError: string;
  registerPasswordError: string;
  formErrors = { name:"",start:"",duration:""};
  //loginEmail: string;
  //loginPassword: string;
  //for testing
  loginEmail = 'meganmckenzie@gmail.com';
  loginPassword = '^Z2AwhuJ)T';
  registerEmail: string;
  registerPassword: string;
  organiser: string;
  event: string;
  signingUp = false;

  agendaForm: FormGroup;
  //formMsg: string;
  options = {
    placeholder: "+ track",
    secondaryPlaceholder: "Enter a track (optional)"
  };

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
      duration: [1,[Validators.required,Validators.pattern('^[1-9]$')]],
      tracks: [[]]
    });
  }

  /*private clearMsg = () => {
    setTimeout(()=>{this.successMsg = undefined;},3000);
  };*/

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
    this.dashBoardService.signUp(this.registerEmail, this.registerPassword,this.organiser,this.event).subscribe(
      status => { 
        if (status === 201){ 
          //this.successMsg = 
          'Sign Up success! Please check your email and click on the verification link.';
          this.toggleSigningUp();
        }
      },
      error =>  {
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
    this.dashBoardService.logIn(this.loginEmail, this.loginPassword).subscribe(
      success => { 
        this.getAgendas();
      },
      error => {
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
    this.dashBoardService.getAgendas().subscribe(
      (data: Agenda[]) => {
        console.log(data);
        this.agendas = _.sortBy(data, agenda => -agenda.id);
      },
      error => {
       console.log(error);
      }
    );
  }

  submitAgendaForm() {
    console.log(this.agendaForm.value);
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
    this.dashBoardService.createAgenda(this.agendaForm.value.name, this.agendaForm.value.description, this.agendaForm.value.location, this.agendaForm.value.start, this.agendaForm.value.duration, this.agendaForm.value.tracks).subscribe(
      data => { 
        //this.successMsg = 'New agenda created!';
        this.agendas.unshift(data);
      },
      error => {

      }
    );
  }

  onSelect(agenda: Agenda) {
    this.router.navigate(['/agenda', agenda.id]);
  }

  toggleSigningUp() {
    this.signingUp = !this.signingUp;
  }

}
