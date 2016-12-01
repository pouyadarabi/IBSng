/*

    Modifies the Date object to make it
    switchable between Jalali and Gregorian.

    Copyright (C) 2001  ParsPooyesh Co.


  * 2004-12-16 by Mohsen Hariri
            First Release.

*/

// This global variable sets if the Date object work
// in Jalali mode or Gregorian mode
window.DateType = 'J'; // 'G' ;

// save old functions
Date.prototype.__old_getDate = Date.prototype.getDate;
Date.prototype.__old_getDay = Date.prototype.getDay;
Date.prototype.__old_getMonth = Date.prototype.getMonth;
Date.prototype.__old_getYear = Date.prototype.getYear;
Date.prototype.__old_getFullYear = Date.prototype.getFullYear;

Date.prototype.__old_setDate = Date.prototype.setDate;
Date.prototype.__old_setDay = Date.prototype.setDay;
Date.prototype.__old_setMonth = Date.prototype.setMonth;
Date.prototype.__old_setYear = Date.prototype.setYear;
Date.prototype.__old_setFullYear = Date.prototype.setFullYear;


//function to convert gregorian to jalali
Date.prototype.convertToJalali = function(){
    var r = gregorian_to_jalali(this.__old_getFullYear(), this.__old_getMonth()+1, this.__old_getDate());
    r[1] --; // month starts from 0
    return r;
}


//function to set the object to a Jalali date
Date.prototype.setJalaliDate = function(jd){
    var r = jalali_to_gregorian(jd[0], jd[1]+1, jd[2]);
    r[1] --; // month starts from 0
    this.__old_setDate(r[2]);   // preserve this order! otherwise it doesn't
    this.__old_setMonth(r[1]);  // work!(took me a day to find out :(( )
    this.__old_setFullYear(r[0]);
}

// now override anything you want :D
Date.prototype.getDate = function(){
                                        if(this.DateType != 'J')
                                            return this.__old_getDate();

                                        var ret = this.convertToJalali();
                                        return ret[2];
                                     }

Date.prototype.getMonth = function(){
                                        if(this.DateType != 'J')
                                            return this.__old_getMonth();

                                        var ret = this.convertToJalali();
                                        return ret[1];
                                     }

Date.prototype.getYear = function(){
                                        if(this.DateType != 'J')
                                            return this.__old_getYear();

                                        var ret = this.convertToJalali();
                                        var x = ret[0].toString();
                                        return x.substr(2);
                                     }

Date.prototype.getFullYear = function(){
                                        if(this.DateType != 'J')
                                            return this.__old_getFullYear();

                                        var ret = this.convertToJalali();
                                        return ret[0];
                                     }

Date.prototype.setDate = function(p){
                                        if(this.DateType != 'J')
                                            return this.__old_setDate(p);

                                        var ret = this.convertToJalali();
                                        ret[2] = p;
                                        this.setJalaliDate(ret);
                                     }

Date.prototype.setMonth = function(p){
                                        if(this.DateType != 'J')
                                            return this.__old_setMonth(p);

                                        var ret = this.convertToJalali();
                                        ret[1] = p;
                                        this.setJalaliDate(ret);
                                     }
Date.prototype.setYear = function(p){
                                        if(this.DateType != 'J')
                                            return this.__old_setYear(p);

                                        var ret = this.convertToJalali();
                                        ret[0] = 1300 + p;
                                        this.setJalaliDate(ret);
                                     }
Date.prototype.setFullYear = function(p){
                                        if(this.DateType != 'J')
                                            return this.__old_setFullYear(p);

                                        var ret = this.convertToJalali();
                                        ret[0] = p;
                                        this.setJalaliDate(ret);
                                     }

Date.prototype.setType = function(c){
                                        if(!c)
                                            alert("jdate.js : invalid date type! ("+c+")");
                                        else
                                            this.DateType = c;
                                    }