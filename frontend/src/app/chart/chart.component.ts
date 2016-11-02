import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'lodash';

@Component({
  selector: 'line-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class LineChartComponent implements OnInit {
  @Input()
  dataX: string[];
  @Input()
  dataY: number[];
  @Input()
  dataType: string;

  isEmpty: boolean;

  ngOnInit() {
    if(this.dataType == null) {
      this.dataType = 'item';
    }
    this.lineChartData = [
      {
        data: this.dataY, 
        cubicInterpolationMode: 'monotone', 
        label: 'New bookmarks'
      },
      {
        data: this.getCumulativeCount(this.dataY), 
        cubicInterpolationMode: 'monotone', 
        label: 'Cumulative no. of bookmarks'
      }
    ];
    this.lineChartLabels = this.dataX;
    this.isEmpty = _.sum(this.dataY) === 0;
  }

  // lineChart
  public lineChartData:Array<any>;
  public lineChartLabels:Array<any>;
  public lineChartOptions:any = {
    animation: false,
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      yAxes: [{
        ticks: {
          min: 0,
          suggestedMin: 0
        }
      }]
    }
  };
  public lineChartColors:Array<any> = [
    // colorPrimary = 'rgba(65,182,171,1)';
    // colorSecondary = 'rgba(177,201,195,1)';
    {
      backgroundColor: 'rgba(65,182,171,0.2)',
      borderColor: 'rgba(65,182,171,1)',
      pointBackgroundColor: 'rgba(65,182,171,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(65,182,171,0.8)'
    },
    {
      backgroundColor: 'rgba(177,201,195,0.2)',
      borderColor: 'rgba(177,201,195,1)',
      pointBackgroundColor: 'rgba(177,201,195,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(177,201,195,0.8)'
    }
  ];
  public lineChartLegend:boolean = true;
  public lineChartType:string = 'line';

  getCumulativeCount(input: number[]) {
    let copy = _.cloneDeep(input);
    _.reduce(copy, function(sum: number, n: number, index: number) {
      return copy[index] = sum + n;
    }, 0);
    return copy;
  }

  // events
  public chartClicked(e:any):void {
    // console.log(e);
  }

  public chartHovered(e:any):void {
    // console.log(e);
  }
}