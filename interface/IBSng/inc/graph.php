<?php
require_once("init.php");

function getJPGraphPath()
{ /* return path of jpgraph files.
    jpgraph for php version 4 and 5 are diffrent */
    global $jpgraph_ver;
    if(version_compare(phpversion(), "5.0.0") == -1)
    {
        $jpgraph_ver = 1;
        return JPGRAPH_ROOT."jpgraph-1.19/src/";
    }
    else
    {
        $jpgraph_ver = 2;
        return JPGRAPH_ROOT."jpgraph-2.0beta/src/";
    }
}

include_once(getJPGraphPath()."jpgraph.php");
include_once(getJPGraphPath()."jpgraph_line.php");
include_once (getJPGraphPath()."jpgraph_pie.php");
include_once (getJPGraphPath()."jpgraph_pie3d.php");

$SCALE_INTERVALS = array("minute"=>30,
                       "hour"=>5*60,
                       "day"=>1800,
                       "week"=>4*3600,
                       "month"=>12*3600,
                       "year"=>7*24*3600);

function cropValuesForScale($scale,&$dates,&$values)
{
    if($scale == "minute" and sizeof($dates) > 140)
    {
        $dates = array_slice($dates,sizeof($dates)-140);
        $values = array_slice($values,sizeof($values)-140);
    }
    return array($dates,$values);
}

function test()
{
    $a=new IBSGraph( array(time()+1,time()+30,time()+60,time()+90,time()+120), array(1,50,100,20,30) );
    $a->setTitles("A","B","C","D");
    $g = $a->createGraph();
    $g->stroke();
}

class IBSGraph
{
    function IBSGraph(&$dates, &$values, $scale=null)
    {
        assert(sizeof($dates) == sizeof($values));
        
        if(is_null($scale) or !$this->checkScale($scale))
            $scale = $this->autoScale($dates);
                
        $this->scale = $scale;
        
        $this->interval = $this->getScaleInterval($this->scale);

        $this->dates = $dates;
        $this->values = $values;
        
        $this->title = "";
        $this->legend = "";
        $this->xtitle = "";
        $this->ytitle = "";
    }
    
    function setTitles($title, $legend, $xtitle, $ytitle)
    {
        $this->title = $title;
        $this->legend = $legend;
        $this->xtitle = $xtitle;
        $this->ytitle = $ytitle;
    }

    function createGraph($add_text_values = TRUE, $pad_dates=TRUE)
    {/*Create graph using defaults,
        if $add_text_values is true, add current min max and average value to graph*/

        list($dates, $values) = $this->fixValuesByScale($this->dates,$this->values,$this->interval, TRUE);
        list($dates, $values) = $this->fixDatas($dates,$values,$this->interval,$pad_dates);
        $dates = $this->convToLable($dates);

        $graph = $this->_createGraphObj();

        $graph->SetScale("textint");
        $graph->yaxis->scale->SetGrace(50); 
        $graph->yaxis->scale->SetAutoMin(0); 

        $this->_setAxisParams($graph);
        $this->_addTitles($graph);
        
        $graph->xaxis->SetLabelAngle(90);
        $graph->xaxis->SetTickLabels($dates);
        $graph->xaxis->SetTextLabelInterval(5); 
    
        if($add_text_values)
            $this->addTextValues($graph);

        $p1 = $this->createLinePlot($values);
        $graph->Add($p1);
        return $graph;
    }
    
    //////////////////////////////////////////////////////
    function convToLable(&$dates)
    { /*convert epoch dates to human readable format */
        $ndates = array();
        foreach($dates as $date)
            $ndates[] = $this->__getDateLable($date);
        return $ndates;
    }   
    
    function __getDateLable($date)
    {
        switch($this->scale)
        {
            case "minute":
            case "hour":
                return strftime("%H:%M",(int)$date);
                break;

            case "day":
            case "week":
                return strftime("%d %H:%M",(int)$date);
                break;

            case "month":
                return strftime("%m/%d",(int)$date);
                break;

            case "year":
                return strftime("%y/%m/%d",(int)$date);
                break;

            default:
                return $date;
                break;
        }
    }

    ////////////////////////////////////////
    function _createGraphObj()
    {
        $graph = new Graph(735,450,"auto");

        $graph->img->SetMargin(45,120,40,70);
        $graph->SetShadow();
        $graph->SetGridDepth(DEPTH_FRONT);
//      $graph->SetAlphaBlending();
        $graph->SetMarginColor('white'); 
        $graph->SetFrame(false);        

        return $graph;    
    }
    
    function _addTitles(&$graph)
    {
//      $graph->title->SetFont(FF_FONT1,FS_BOLD);
//      $graph->title->Set($this->title);
        $graph->tabtitle->Set($this->title);
        $graph->tabtitle->SetFillColor('white'); 
//      $graph->tabtitle->SetFont(FF_ARIAL,FS_BOLD,13);

        $graph->xaxis->title->Set($this->xtitle);
        $graph->yaxis->title->Set($this->ytitle);
        $graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD);
        $graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD);

        $graph->legend->SetShadow('gray@0.4',5);

    }
    
    function _setAxisParams(&$graph)
    {
        $graph->yaxis->HideZeroLabel();
        $graph->ygrid->SetFill(true,'#EFEFEF@1','#EFEFEF@.9');
//      $graph->ygrid->SetFill(true,'white','white');
        $graph->xaxis->SetLabelAngle(90);
        $graph->yaxis->SetTitlemargin(33); 
    }

    function createLinePlot(&$values)
    {
        $p1 = new LinePlot($values);
        $p1->SetColor("black");
        $p1->SetFillColor("#990000");

        $p1->SetLegend($this->legend);
        $p1->SetStepStyle();
        return $p1;
    }

    ///////////////////////////////////////////////
    function addTextValues(&$graph)
    {/*
        add cur max min and average texts to graph
    */
        $cur=price($this->values[sizeof($this->values)-1]);
        $max=price(max($this->values));
        $min=price(min($this->values));
        $avg=price(array_sum($this->values)/sizeof($this->values));
        $this->addStatisticalValuesToGraph($graph,$cur,$min,$max,$avg);
    }
    ////////////////////////////////////////////////

    function addStatisticalValuesToGraph(&$graph,$cur,$min,$max,$avg)
    {
        $txt=new Text("Cur: {$cur}\nMin: {$min}\nMax: {$max}\nAvg: {$avg}\nScale: ".ucwords($this->scale));
        $txt->SetPos(620,0.5,"left","left");
        $txt->SetFont(FF_FONT1,FS_BOLD);
        $txt->ParagraphAlign('left');
        $txt->SetBox('#EBEBEB','black','gray');
        $txt->SetShadow('gray',7);
        $graph->AddText($txt);
    }


    ///////////////////////////////////////////
    function checkScale($scale)
    {/* check if scale $scale is valid */
        global $SCALE_INTERVALS;
        if(isset($SCALE_INTERVALS[$scale]))
            return TRUE;
        else
            return FALSE;
    }


    function autoScale(&$dates)
    { /* determine the best scale for $dates array and return it */
        $delta = $dates[sizeof($dates)-1] - $dates[0];
        if ($delta <= 3600*2)
            return "minute";
        else if ($delta <= 3600*12)
            return "hour";
        else if ($delta <= 3600*24*5)
            return "day";
        else if ($delta <= 3600*24*25)
            return "week";
        else if ($delta <= 3600*24*60)
            return "month";
        else
            return "year";
    }
    
    function getScaleInterval($scale)
    {
        global $SCALE_INTERVALS;
        return $SCALE_INTERVALS[$scale];
    }

    //////////////////////////////////////////////
    function fixDatas(&$dates, &$values, $interval, $pad_dates=TRUE, $shift_dates=FALSE)
    {/* pad datas to have at least 60 data for graph 
        $pad_dates(boolean): pad dates to have at least 60 values
        $shift_dates(boolean): shift datas, so they would be starting at five minutes. This make 
                              X axis label cleaner
    */
        if(!sizeof($dates))
        {
            $dates[0] = time();
            $values[0] = 0;
        }

        while($pad_dates and sizeof($dates)<60)
        {
            array_unshift($dates,$dates[0]-$interval);
            array_unshift($values,0);
        }
        
        if ($shift_dates)
        {
            while($dates[0]%300)
            {
                array_shift($dates);
                array_shift($values);
            }
        }
        
        return array($dates,$values);
    }


    //////////////////////////////////////////////////////////

    function fixValuesByScale(&$dates, &$values, $interval, $round)
    { /* $dates(array): array of dates in epoch
         $values(array): array of values
         $interval(int): interval of output
         $round(boolean): round the values?
         
         convert $dates to be in interval of $interval. this make graph easy to handle
         and clean
      */
        $ndates = array();
        $nvalues = array();
        
        $i = sizeof($dates)-1;
        if($i<0)
            return array(array(),array());
            
        $cur = $dates[$i] - $dates[$i]%$interval;
        
        while($i>=0)
        {
            $c = 0;
            $sum = 0;
            do
            {
                $sum += $values[$i];
                $c++;
                $i--;
            }while ($i > 0 and $dates[$i] > $cur - $interval);

            $ndates[] = $cur;
            
            if ($round)
                $nvalues[] = round( $sum/$c );
            else
                $nvalues[] = $sum/$c ;
                
            $cur -= $interval;

            while($i>=0 and $dates[$i] < $cur - $interval)
            {
                $ndates[] = $cur;
                $val = $this->calcDateValue($dates[$i+1],$dates[$i],$values[$i+1],$values[$i],$cur);

                if($round)
                    $nvalues[] = round($val);
                else
                    $nvalues[] = $val;
                    
                $cur -= $interval;
            }

        }
    
        return array ( array_reverse($ndates), array_reverse($nvalues) );
    }

    function calcDateValue($d2, $d1, $v2, $v1, $d)
    {/*
        calculate value of date $d, using the previous and next value
        this is done by drawing! a line between them and calculate value of line in $d
    */
        $a = ($v2 - $v1)/($d2 - $d1);
        $b = $v2 - $a * $d2;
        return $a * $d + $b;
    }

}

class IBSBWGraph extends IBSGraph
{
    function setTitles($title, $legend1, $legend2, $xtitle, $ytitle)
    {
        $this->title = $title;
        $this->legend1 = $legend1;
        $this->legend2 = $legend2;
        $this->xtitle = $xtitle;
        $this->ytitle = $ytitle;
    }


    function createGraph($add_text_values = TRUE)
    {/*Create graph using defaults,
        if $add_text_values is true, add current min max and average value to graph*/

        list($in_vals,$out_vals) = $this->separateBwVals();

        list($dates, $in_vals) = $this->fixValuesByScale($this->dates,$in_vals,$this->interval, FALSE);
        list($dates, $out_vals) = $this->fixValuesByScale($this->dates,$out_vals,$this->interval, FALSE);

        $ndates = $dates;
        list($ndates, $in_vals) = $this->fixDatas($ndates,$in_vals,$this->interval);
        list($dates, $out_vals) = $this->fixDatas($dates,$out_vals,$this->interval);
        
        $dates = $this->convToLable($dates);

        $graph = $this->_createGraphObj();

        $graph->SetScale("textlin");
        $graph->yaxis->scale->SetGrace(50); 
        $graph->yaxis->scale->SetAutoMin(0); 

        $this->_setAxisParams($graph);
        $this->_addTitles($graph);
        
        $graph->xaxis->SetTickLabels($dates);
        $graph->xaxis->SetTextLabelInterval(5); 
    
        if($add_text_values)
            $this->addTextValues($graph,$in_vals,$out_vals);

        $p1 = $this->createLinePlot($in_vals, "#990000", $this->legend1, TRUE);
        $p2 = $this->createLinePlot($out_vals, "#FFAA00", $this->legend2);

        $graph->Add($p1);
        $graph->Add($p2);
        return $graph;
    }

    function separateBwVals()
    {
        $in_vals = array(); $out_vals = array();
        foreach($this->values as $val)
        {
            $in_vals[] = $val[0]/1024.0;
            $out_vals[] = $val[1]/1024.0;
        }
        return array($in_vals, $out_vals);
    }

    function createLinePlot(&$values,$color, $legend,$fill=FALSE)
    {
        $p = new LinePlot($values);
        $p->SetColor($color);
        if($fill)
            $p->SetFillColor("{$color}");

        $p->SetWeight(2.5);
        $p->SetLegend($legend);
        return $p;
    }


    ///////////////////////////////////////////////
    function addTextValues(&$graph,&$in_vals,&$out_vals)
    {/*
        add cur max min and average texts to graph
    */
        $cur_in=price($in_vals[sizeof($in_vals)-1],0);
        $cur_out=price($out_vals[sizeof($out_vals)-1],0);

        $max_in=price(max($in_vals),0);
        $min_in=price(min($in_vals),0);

        $max_out=price(max($out_vals),0);
        $min_out=price(min($out_vals),0);
        
        $avg_in=price(array_sum($in_vals)/sizeof($in_vals),1);
        $avg_out=price(array_sum($out_vals)/sizeof($out_vals),1);
        
        $this->addStatisticalValuesToGraph($graph,$cur_in,$cur_out,$min_in,$min_out,$max_in,$max_out,$avg_in,$avg_out);
    }

    function addStatisticalValuesToGraph(&$graph,$cur_in,$cur_out,$min_in,$min_out,$max_in,$max_out,$avg_in,$avg_out)
    {
        $txt=new Text("Unit: kb/s\n\nCur In: {$cur_in}\nCur Out: {$cur_out}\n\nMin In: {$min_in}\nMin Out: {$min_out}\n\nMax In: {$max_in}\nMax Out: {$max_out}\n\nAvg In: {$avg_in}\nAvg Out: {$avg_out}\n\nScale: ".ucwords($this->scale));
        $txt->SetPos(625,180,"left","left");
        $txt->SetFont(FF_FONT1,FS_BOLD);
        $txt->ParagraphAlign('left');
        $txt->SetBox('#EBEBEB','black','gray');
        $txt->SetShadow('gray',7);
        $graph->AddText($txt);
    }


}

class IBSPieGraph
{
    function IBSPieGraph($title, &$legends, &$labels,&$datas)
    {
        $this->title=$title;
        $this->legends=$legends;
        $this->labels=$labels;
        $this->datas=$datas;
    }
    
    function createGraph()
    {
        $graph = new PieGraph(600,500,"auto");
        $graph->SetShadow();
        $graph->title->Set($this->title);
        $graph->title->SetFont(FF_FONT1,FS_BOLD);
        $p1 = new PiePlot($this->datas);
        $p1->SetSize(0.3);
        $p1->SetCenter(0.45);
        $p1->SetLegends($this->legends);
        $p1->SetLabelType(PIE_VALUE_PER);
        $p1->SetLabels($this->labels,"auto");
        $p1->value->SetFont(FF_FONT1,FS_BOLD);
        $p1->value->SetColor("darkred");
        $p1->value->Show();
        $p1->SetShadow();
//      $p1->SetTheme("sand");
        $p1->ExplodeAll(8);
        $graph->Add($p1);
        return $graph;
    }
}