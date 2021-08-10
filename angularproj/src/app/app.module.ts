import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
// import { MainComponent } from './main/main.component';
// import { AddpostComponent } from './addpost/addpost.component';
// import { PostComponent } from './post/post.component';

import { HttpClientModule } from '@angular/common/http'


@NgModule({
  declarations: [
    AppComponent

    // MainComponent,
    // AddpostComponent,
    // PostComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
