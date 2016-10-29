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
  errorMsg: string;
  successMsg: string;
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
  formMsg: string;
  options = {
    placeholder: "+ track",
    secondaryPlaceholder: "Enter a track (optional)"
  };

  ngOnInit() {
    this.agendaForm = this._fb.group({
      name: ['', [<any>Validators.required]],
      description: '',
      location: '',
      start: ['', Validators.required],
      duration: 3,
      website: '',
      tracks: [[]],
    });
    if (this.user.authed) {
      this.getAgendas();
    }
  }

  private clearMsg = (success: boolean) => {
    if(success) {
      setTimeout(()=>{this.successMsg = undefined;},3000);
    }else{
      setTimeout(()=>{this.errorMsg = undefined;},3000);
    }
  };
  
  signUp() {
    if (!this.registerEmail || !this.registerPassword) { 
      this.errorMsg = "Please enter email and password";
      return;
    }
    this.dashBoardService.signUp(this.registerEmail, this.registerPassword,this.organiser,this.event).subscribe(
      status => { 
        if (status === 201){ 
          this.successMsg = 
          'Sign Up success! Please check your email and click on the verification link.';
          this.clearMsg(true);
          this.toggleSigningUp();
        }
      },
      error =>  {
        this.errorMsg = <any>error;
        this.clearMsg(false);
      }
    );
  }

  logIn() {
    if (!this.loginEmail || !this.loginPassword) { 
      this.errorMsg = "Please enter email and password";
      this.clearMsg(false);
      return;
    }
    this.dashBoardService.logIn(this.loginEmail, this.loginPassword).subscribe(
      success => { 
        this.successMsg = "Login success!"; 
        //this.open();
        this.clearMsg(true);
        this.getAgendas();
      },
      error => {
        this.errorMsg = <any>error;
        this.clearMsg(false);
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
       this.errorMsg = <any>error;
       this.clearMsg(false);
      }
    );
  }

  submitAgendaForm(isValid: boolean) {
    if (!isValid) { 
      this.formMsg = "Please fill in Name and Start Date";
      return;
    }
    console.log(this.agendaForm.value);
    this.createAgenda();
  }

  createAgenda() {
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
      this.agendaForm.value.tracks,
    ).subscribe(
      data => { 
        this.formMsg = 'New agenda created!';
        this.agendas.unshift(data);  // New agendas are added to the top
      },
      error => this.formMsg = <any>error
    );
  }

  onSelect(agenda: Agenda) {
    this.router.navigate(['/agenda', agenda.id]);
  }

  toggleSigningUp() {
    this.signingUp = !this.signingUp;
  }
}
