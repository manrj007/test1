import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-left-panel',
  templateUrl: './left-panel.component.html',
  styleUrls: ['./left-panel.component.scss']
})
export class LeftPanelComponent implements OnInit {
  tabs: any[] =[];
  constructor() { }

  ngOnInit() {
    this.tabs = [ 
      { name: 'Preview', router: '/main', icon: 'movie' },
      { name: 'Upload Docs', router: '/compare', icon: 'attach_file' }
    ]
  }

  showInfo() {

  }

}
