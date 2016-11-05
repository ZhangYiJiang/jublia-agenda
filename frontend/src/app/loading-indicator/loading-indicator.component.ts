import {Component, Input} from '@angular/core';

@Component({
  selector: 'loading-indicator',
  template: `
    <div class="loading-overlay" [class.backdrop]="overlay">
      <i class="fa fa-spinner fa-pulse fa-5x fa-fw"></i>
      <span class="sr-only">Loading</span>
    </div>`,
  // Most of the styles for this class are declared in styles.scss 
  // since this indicator is also used for the initial loading screen
  styles: [`
    .backdrop {
      background: rgba(0, 0, 0, 0.6);
    }
  `],
})

export class LoadingIndicatorComponent {
  @Input() overlay = false;
}