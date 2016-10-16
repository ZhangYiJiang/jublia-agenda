import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpModule } from '@angular/http';
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
  private dashBoardService: DashBoardService,
  private agendaService: AgendaService) { }

  agendas = this.dashBoardService.agendas;
  user = this.dashBoardService.user;
  errorMsg: string;
  successMsg: string;
  loginEmail: string;
  loginPassword: string;
  registerEmail: string;
  registerPassword: string;
  organiser: string;
  event: string;
  signingUp = false;

  ngOnInit() {
    if (this.user.authed) {
      this.getAgendas();
    }
  }

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
          this.toggleSigningUp();
        }
      },
      error =>  this.errorMsg = <any>error
    );
  }

  logIn() {
    if (!this.loginEmail || !this.loginPassword) { 
      this.errorMsg = "Please enter email and password";
      return;
    }
    this.dashBoardService.logIn(this.loginEmail, this.loginPassword).subscribe(
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

  onSelect(agenda: Agenda) {
    this.router.navigate(['/agenda', agenda.id]);
  }

  toggleSigningUp() {
    this.signingUp = !this.signingUp;
  }
}
