import { Component } from '@angular/core';
import '../../public/css/styles.css';

import { GlobalVariable } from './globals';

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  appName: string = GlobalVariable.APP_NAME;
}
