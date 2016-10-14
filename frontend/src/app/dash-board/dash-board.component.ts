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

  ngOnInit() {
    /*this.agendaService.getAgendas()
    .then((agendas: Agenda[]) => {
      //console.log(agendas);
      this.agendas.push(...agendas);
    })*/
    if (this.user.authed) {
      this.getAgendas();
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

  logOut() {
    this.dashBoardService.logOut();
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
}
