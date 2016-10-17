import { Component, OnInit, ViewContainerRef } from '@angular/core';
import {MdSnackBar, MdSnackBarConfig} from '@angular/material';
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
    private agendaService: AgendaService,
    public snackBar: MdSnackBar,
    public viewContainerRef: ViewContainerRef
  ){}

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

  open() {
    let config = new MdSnackBarConfig(this.viewContainerRef);
    this.snackBar.open(this.successMsg, null,config);
  }
  private clearMsg = (success: boolean) => {
    if(success) {
      setTimeout(()=>{this.successMsg = undefined;},3000);
    }else{
      setTimeout(()=>{this.errorMsg = undefined;},3000);
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
          this.clearMsg(true);
          this.toggleSigningUp();
        }
      },
      error =>  {
        this.errorMsg = <any>error
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
      data => {
        console.log(data);
        this.agendas = [];
        this.agendas.push(...data);
      },
      error => {
       this.errorMsg = <any>error;
       this.clearMsg(false);
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
