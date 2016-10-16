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
  private agendaService: AgendaService) { }

  agendas = this.dashBoardService.agendas;
  user = this.dashBoardService.user;
  errorMsg: string;
  successMsg: string;

  agendaForm: FormGroup;
  formMsg: string;
  options = {
    placeholder: "+ track",
    secondaryPlaceholder: "Enter a new track (optional)"
  }

  ngOnInit() {
    if (this.user.authed) {
      this.getAgendas();

      this.agendaForm = this._fb.group({
            name: ['', [<any>Validators.required]],
            abstract: [''],
            location: [''],
            start: ['', [<any>Validators.required]],
            end: [''],
            tracks: [[]]
      });
    }
  }

  signUp(email: string, password: string) {
    if (!email || !password) { 
      this.errorMsg = "Please enter email and password";
      return;
    }
    this.dashBoardService.signUp(email, password).subscribe(
      status => { if (status === 201) this.successMsg = 
        'Sign Up success! Please check your email and click on the verification link.' },
      error =>  this.errorMsg = <any>error
    );
  }

  logIn(email: string, password: string) {
    if (!email || !password) { 
      this.errorMsg = "Please enter email and password";
      return;
    }
    this.dashBoardService.logIn(email, password).subscribe(
      success => { this.successMsg = "Login success!"; this.getAgendas(); },
      error =>  this.errorMsg = <any>error
    );
  }

  getAgendas() {
    this.dashBoardService.getAgendas().subscribe(
      data => {
        console.log(data);
        this.agendas = [];
        this.agendas.push(...data)
      },
      error =>  this.errorMsg = <any>error
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
    this.dashBoardService.createAgenda(this.agendaForm.value.name, this.agendaForm.value.abstract, this.agendaForm.value.location, this.agendaForm.value.start).subscribe(
      data => { 
        this.formMsg = 'New agenda created!';
        this.agendas.push(data);
        for (let track of this.agendaForm.value.tracks) {
          this.createTrack(data.id, track);
        }
      },
      error =>  this.formMsg = <any>error
    );
  }

  createTrack(agendaId: number, name: string) {
    this.dashBoardService.createTrack(agendaId, name).subscribe(
      success => console.log('new track created'),
      error =>  this.formMsg = <any>error
    );
  }

  onSelect(agenda: Agenda) {
    this.router.navigate(['/agenda', agenda.id]);
  }
}
