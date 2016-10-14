import {Pipe, PipeTransform} from '@angular/core';

@Pipe({ name: 'where', pure: false })
export class Where implements PipeTransform {
  tmp: any[] = [];
  static _whereComparer(a: any, b: any): boolean {
    if (a && b) {
      for (let p in b) {
        if (a[p] != b[p])
          return false;
      }
      return true;
    }
    return false;
  }

  transform(input: any, args: any): any {
    this.tmp.length = 0;
    let clauses = args;
    if (input){
      this.tmp.push(...input.filter((item: any) => Where._whereComparer(item, clauses)));
    }
    return this.tmp; 
  }
}