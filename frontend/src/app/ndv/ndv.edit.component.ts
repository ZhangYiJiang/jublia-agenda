import {Component, Input, EventEmitter, ElementRef, HostListener} from '@angular/core';


@Component({
    selector: 'ndv-edit',
    styles: [`
        :host {
            position: relative;
        }
        
        .ndv-ic {
            position: absolute;
            top: 0;
            left: -1px;
            transform: translateY(-100%);
            padding: 3px 6px 3px 4px;
            
            background: #888;
            color: #fff;
            font-size: 13px;
            line-height: 1;
            font-weight: normal;
            white-space: nowrap;
            
            display: none;
        }
        
        .ndv-comp:hover .ndv-ic {
            display: block;
        }

        .ndv-comp {
            padding: 6px;
            border-radius: 3px;
            border: 1px solid #ccc;
            min-width: 50px;
            display: inline-block;
            position: relative;
        }
        
        .ndv-comp:hover {
            border-radius: 0 3px 3px 3px;
        }
        
        .active-ndv {
            background-color: #f0f0f0;
            border: 1px solid #d9d9d9;
        }
        
        form {
            display: inline;
        }
        
        input {
            border-radius: 5px;
            box-shadow: none;
            border: 1px solid #dedede;
            min-width: 5px;
        }
        
        .ndv-buttons {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-top: none;
            border-radius: 0 0 3px 3px;
            box-shadow: 0 3px 6px rgba(111,111,111,0.2);
            outline: none;
            padding: 3px;
            position: absolute;
            width: 80px;
            left: 6px;
            top: 100%;
            z-index: 1;
            font-size: 1.1rem;
            line-height: 1.5rem;
        }
        
        .ndv-comp:hover {
            border-color: #999;
        }
        
        .ng-invalid {
            background: #ffb8b8;
            border-color: red;
        }
        
        .err-bubble {
            position: absolute;
            border: 1px solid red;
            font-size: 14px;
            background: #ffb8b8;
            padding: 6px 12px;
            width: 200px;
            line-height: 1.3;
            left: 0;
            top: 0;
            transform: translateY(calc(-100% - 10px));
        }
    `],
    template: `<span *ngIf="!permission">{{text}}</span>
               <span *ngIf="permission" class='ndv-comp' (click)='makeEditable()' [ngClass]="{'ndv-active':show}">
                   <form (submit)="callSave($event)">
                       <input *ngIf='show' [ngClass]="{'ng-invalid': invalid}" (ngModelChange)="validate($event)" 
                              type='text' [(ngModel)]='text' [ngModelOptions]="{standalone: true}" />
                       <div class='err-bubble' *ngIf="invalid">{{error || " must contain " + min + " to -" + max +" chars."}}</div>
                       <span class='ndv-ic' *ngIf='!show'>✎ Edit</span>
                       <span *ngIf='!show'>{{text || 'Empty'}}</span>
                   
                       <span class='ndv-buttons' *ngIf='show'>
                           <a class='button primary button-symbol' (click)='callSave($event)'><i class="fa fa-check fa-fw" aria-hidden="true"></i></a>
                           <a class='button secondary button-symbol' (click)='callCancel($event)'><i class="fa fa-times fa-fw" aria-hidden="true"></i></a>
                       </span>
                   </form>
               </span>`,
    host: {
        "(document: click)": "compareEvent($event)",
    },
    outputs: ['save : onSave']
})

export class NdvEditComponent {
    @Input('placeholder') text: any;
    @Input('title') fieldName: any;
    originalText: any;
    editedText: any;
    tracker: any;
    el: ElementRef;
    show = false;
    save = new EventEmitter;
    @Input() permission = false;
    @Input() min = 0;
    @Input() max = 10000;
    @Input() error: any;
    @Input() regex: any;
    invalid = false;

    constructor(el: ElementRef) {
        this.el = el;
    }
    
    ngOnInit() {
        this.originalText = this.text;    //Saves a copy of the original field info.
    }

    validate(text: any) {
        if (this.regex) {
            var re = new RegExp('' + this.regex, "ig");
            this.invalid = !re.test(text);
        } else {
            this.invalid = text.length > this.max || text.length < this.min;
        }
        //console.log(this.invalid);
    }

    makeEditable() {
        if (this.show == false) {
            // Restore the user's last saved text, if possible
            if (this.editedText) {
                this.text = this.editedText;
            }
            
            this.show = true;
        }
    }

    compareEvent(globalEvent: any) {
        if (this.tracker != globalEvent && this.show) {
            this.cancelEditable();
        }
    }

    @HostListener('click', ['$event']) trackEvent(newHostEvent: any) {
        this.tracker = newHostEvent;
    }

    cancelEditable(resetInput: boolean = false) {
        // Save a copy of the text the user was editing
        if (!resetInput) {
            this.editedText = this.text;
        } else {
            this.editedText = null;
        }
        
        this.show = false;
        this.invalid = false;
        this.text = this.originalText;
    }

    callCancel(evt: any) {
        this.cancelEditable(true);
        evt.stopPropagation();
    }

    callSave(evt: any) {
        if (!this.invalid) {
            const text = this.text;
            const data = {};  //BUILD OBJ FOR EXPORT.
            data["" + this.fieldName] = text;
            
            setTimeout(() => {
                this.editedText = null;
                this.originalText = text;
                this.text = text;
            }, 0);  //Sets the field with the new text;
            
            this.save.emit(data);
            this.show = false;
        }
        
        evt.stopPropagation();
        evt.preventDefault();
    }
}