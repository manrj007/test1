import { NgModule } from "@angular/core";
import { MatToolbarModule, MatIconModule, MatButtonModule, MatListModule, MatCardModule, MatChipsModule, MatFormFieldModule, MatSelectModule, MatDialogModule, MatProgressBarModule, MatTooltipModule, MatRadioModule, MatTableModule, MatTabsModule } from "@angular/material";

@NgModule({
    imports: [
        MatToolbarModule,
        MatIconModule,
        MatButtonModule,
        MatListModule,
        MatCardModule,
        MatChipsModule,
        MatFormFieldModule,
        MatSelectModule,
        MatDialogModule,
        MatProgressBarModule,
        MatTooltipModule,
        MatRadioModule,
        MatTableModule,
        MatTabsModule
    ],
    exports: [
        MatToolbarModule,
        MatIconModule,
        MatButtonModule,
        MatListModule,
        MatCardModule,
        MatChipsModule,
        MatFormFieldModule,
        MatSelectModule,
        MatDialogModule,
        MatProgressBarModule,
        MatTooltipModule,
        MatRadioModule,
        MatTableModule,
        MatTabsModule
    ]
  })
  export class MaterialModule { }