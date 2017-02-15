function Legend(selection) {
    var width = Math.MAX_VALUE,
        legendRectSize = 16,
        legendSpacing = 4,
        colourScale = d3.scale.category20();

    function legend(selection) {
        selection.each(function(data) {

            groups = d3.select(this).selectAll('g')
                .data(data);

            groups.exit().remove();

            groupsEnter = groups.enter().append('g');

            groupsEnter.append('rect')
                .attr('width', legendRectSize)
                .attr('height', legendRectSize);

            groupsEnter.append('text')
                .attr('x', legendRectSize + legendSpacing)
                .attr('y', legendRectSize - legendSpacing)
                .text(function(d) {
                    return d;
                });

            var groupsOffsets = {
                x: 0,
                y: 0
            };
            groups.attr('transform', function(d) {
                    if (this.getBBox().width + groupsOffsets.x > width) {
                        groupsOffsets.x = 0;
                        groupsOffsets.y += this.getBBox().height + legendSpacing;
                    }

                    var x = groupsOffsets.x,
                        y = groupsOffsets.y;
                    groupsOffsets.x += this.getBBox().width + legendSpacing;

                    return 'translate(' + (x + ', ' + groupsOffsets.y + ')');
                }).select('rect')
                .style('fill', function(d, i) {
                    return colourScale(d);
                })
                .style('stroke', function(d, i) {
                    return colourScale(d);
                });
        });
    }

    legend.width = function(_) {
        if (!arguments.length) return width;
        width = _;
        return legend;
    };
    legend.legendRectSize = function(_) {
        if (!arguments.length) return legendRectSize;
        legendRectSize = _;
        return legend;
    };
    legend.legendSpacing = function(_) {
        if (!arguments.length) return legendSpacing;
        legendSpacing = _;
        return legend;
    };
    legend.colourScale = function(_) {
        if (!arguments.length) return colourScale;
        colourScale = _;
        return legend;
    };

    return legend;
}

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//                        Bar chart below                             //
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

function BarChart(selection) {
    // Default values
    var margin = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 120
        },
        width = 1280,
        barHeight = 20,
        gapBetweenGroups = 10,
        drawsLegend = true,
        legend = Legend,
        colourScale = d3.scale.category20(),
        catagoryScale = d3.scale.ordinal(),
        groupScale = d3.scale.ordinal(),
        xScale = d3.scale.linear(),
        highlightSections = [],
        highlightedBars = [],
        valueBoundaries = {
            xMin: undefined,
            xMax: undefined,
            yMin: undefined,
            yMax: undefined
        };

    function chart(selection) {
        selection.each(function(data) {
            var dataset = [];
            var dateCatagories = [];
            var series = [];

            var maxValue = Number.MIN_VALUE,
                minValue = Number.MAX_VALUE;
            data.forEach(function(d) {
                series.push(d.name);
                d.values.forEach(function(value) {
                    var date = new Date(value.date);
                    var i = 0;
                    while (i < dateCatagories.length) {
                        if (dateCatagories[i].getTime() == date.getTime()) {
                            date = dateCatagories[i];
                            break;
                        }
                        i++;
                    }
                    if (i == dateCatagories.length) {
                        dateCatagories.push(date);
                    }

                    maxValue = value.value > maxValue ? value.value : maxValue;
                    minValue = value.value < minValue ? value.value : minValue;
                    dataset.push({
                        name: d.name,
                        date: date,
                        value: value.value,
                        highlightIdentifier: value.highlightIdentifier
                    });
                });
            });
            dateCatagories.sort(function(a, b) {
                return b.getTime() - a.getTime();
            });

            // selects the hierarchy if it exists or creates them.
            var self, svg, tooltip;
            if (d3.select(this).select('.chart-container').empty()) {
                self = d3.select(this).append('div').attr('class', 'chart-container').style('position', 'relative');
                svg = self.append('svg');
                svg.append('g').attr('class', 'chart');
                svg.append('g').attr('class', 'legend');
                tooltip = self.append('div').classed('tooltip hidden', true);
            } else {
                self = d3.select(this).select('.chart-container');
                svg = self.select('svg');
                tooltip = self.select('.tooltip').classed('hidden', true);
            }
            svg.attr("width", width);
            svg.select('g.legend').attr('transform', 'translate(0, ' + margin.top / 2 + ')');

            var legend = svg.select('g.legend');
            legend.datum(!drawsLegend ? [] : data.map(function(d) {
                    return d.name;
                }))
                .call(
                    Legend().width(width)
                    .colourScale(colourScale)
                );

            var legendHeight = legend.node().getBBox().height,
                groupHeight = series.length * barHeight,
                chartHeight = (groupHeight + gapBetweenGroups) * dateCatagories.length;

            svg.attr("height", margin.top + legendHeight + chartHeight + margin.bottom);

            catagoryScale.domain(dateCatagories).rangeRoundBands([0, chartHeight]);
            groupScale.domain(series).rangeRoundBands([0, groupHeight]);
            xScale.domain([minValue, maxValue]).range([0, width - margin.left - margin.right]);

            var yAxis = d3.svg.axis()
                .scale(catagoryScale)
                .tickValues(dateCatagories)
                .tickFormat(d3.time.format('%Y/%m/%d %I%p'))
                .tickSize(0)
                .orient("left");

            svg.select('g.axis')
                .remove();

            svg.append("g")
                .attr("class", "y axis")
                .attr("transform", 'translate(' + margin.left + ' , ' + (margin.top + legendHeight) + ")")
                .call(yAxis);

            var chart = svg.select('g.chart');
            chart.attr("transform", 'translate(' + margin.left + ' , ' + (margin.top + legendHeight) + ")");

            chart.selectAll('.background-rect').remove();
            highlightSections.forEach(function(hs) {
                var minBound = d3.min(dateCatagories.filter(function(d) {
                    return hs.start < d;
                }));
                var maxBound = d3.max(dateCatagories.filter(function(d) {
                    return hs.end > d;
                }));

                chart.insert("rect", ":first-child")
                    .attr({
                        class: 'background-rect',
                        x: 0,
                        y: catagoryScale(maxBound),
                        width: width - margin.left - margin.right,
                        height: catagoryScale(minBound) - catagoryScale(maxBound) + groupHeight + gapBetweenGroups,
                        fill: '#ffffff'
                    });
            });

            if (highlightSections.length > 0) {
                chart.insert("rect", ":first-child")
                    .attr({
                        class: 'background-rect',
                        w: 0,
                        h: 0,
                        width: width - margin.left - margin.right,
                        height: chartHeight,
                        fill: '#DDDDDD'
                    });
            }

            // Create bars
            var bar = chart.selectAll("g")
                .data(dataset, function(d) {
                    return d.name + ':' + d.date.getTime();
                });

            bar.exit().remove();

            // enter
            var barEnter = bar.enter().append("g")
                .attr("transform", function(d) {
                    return "translate(0," + (catagoryScale(d.date) + groupScale(d.name) + gapBetweenGroups / 2) + ")";
                });
            barEnter.append('rect')
                .attr("class", "bar")
                .attr("height", barHeight - 1 + 'px')
                .attr('width', '0px');
            barEnter.append('text')
                .attr("y", barHeight / 2)
                .attr("fill", "red")
                .attr("dy", ".35em")
                .text(function(d) {
                    return Math.floor(d.value);
                })
                .attr('class', 'bar-value');

            //update
            bar.attr("fill", function(d) {
                    return colourScale(d.name);
                })
                .classed('bar-highlight', function(d) {
                    return highlightedBars.indexOf(d.highlightIdentifier) != -1;
                })
                .transition()
                .attr("transform", function(d) {
                    return "translate(0," + (catagoryScale(d.date) + groupScale(d.name) + gapBetweenGroups / 2) + ")";
                });

            var hoverDate = d3.time.format('%Y/%m/%d %H:%M');

            bar.select("rect")
                .on('mouseenter', function(d) {
                    tooltip.classed('hidden', false);
                })
                .on("mousemove", function(d) {
                    var xPos = d3.mouse(svg.node())[0];
                    var yPos = d3.mouse(svg.node())[1];

                    var label = d.name + '<br>Date: ' + hoverDate(d.date) + '<br>Value: ' + Math.floor(d.value);
                    tooltip.html(label);

                    var tooltipX = xPos + 15;
                    if (tooltipX + tooltip.node().getBoundingClientRect().width > width) {
                        tooltipX -= tooltip.node().getBoundingClientRect().width + 30;
                    }
                    tooltip.attr('style', 'position: absolute; left:' + tooltipX + 'px; top:' + (yPos - 35) + 'px');
                })
                .on("mouseout", function() {
                    tooltip.classed('hidden', true);
                })
                .transition().duration(400)
                .attr("width", function(d) {
                    return xScale(d.value) + 'px';
                });

            // Add text label in bar
            bar.select("text")
                .attr("x", function(d) {
                    return xScale(d.value) - 3;
                });
        });
    }

    chart.margin = function(_) {
        if (!arguments.length) return margin;
        margin = _;
        return chart;
    };

    chart.width = function(_) {
        if (!arguments.length) return width;
        width = _;
        return chart;
    };

    chart.barHeight = function(_) {
        if (!arguments.length) return barHeight;
        barHeight = _;
        return chart;
    };

    chart.gapBetweenGroups = function(_) {
        if (!arguments.length) return gapBetweenGroups;
        gapBetweenGroups = _;
        return chart;
    };

    chart.drawsLegend = function(_) {
        if (!arguments.length) return drawsLegend;
        drawsLegend = _;
        return chart;
    };

    chart.legendRectSize = function(_) {
        if (!arguments.length) return legendRectSize;
        legendRectSize = _;
        return chart;
    };

    chart.legendSpacing = function(_) {
        if (!arguments.length) return legendSpacing;
        legendSpacing = _;
        return chart;
    };

    chart.colourScale = function(_) {
        if (!arguments.length) return colourScale;
        colourScale = _;
        return chart;
    };

    chart.catagoryScale = function(_) {
        if (!arguments.length) return catagoryScale;
        catagoryScale = _;
        return chart;
    };

    chart.groupScale = function(_) {
        if (!arguments.length) return groupScale;
        groupScale = _;
        return chart;
    };

    chart.xScale = function(_) {
        if (!arguments.length) return xScale;
        xScale = _;
        return chart;
    };

    chart.highlightSections = function(_) {
        if (!arguments.length) return highlightSections;
        highlightSections = _.map(function(d) {
            return {
                start: new Date(d.start),
                end: new Date(d.end)
            }
        });
        return chart;
    };

    chart.highlightedBars = function(_) {
        if (!arguments.length) return highlightedBars;
        highlightedBars = _;
        return chart;
    };

    chart.valueBoundaries = function(_) {
        if (!arguments.length) return valueBoundaries;
        valueBoundaries = _;
        return chart;
    };

    return chart;
}

////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
//                       Line chart below                             //
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

function LineChart(selection) {
    var margin = {
            top: 20,
            right: 20,
            bottom: 60,
            left: 35
        },
        width = 1280,
        height = 720,
        drawsLegend = true,
        colourScale = d3.scale.category20(),
        xScale = d3.scale.linear(),
        yScale = d3.scale.linear(),
        interpolation = 'linear',
        highlightSections = [],
        valueBoundaries = {
            xMin: undefined,
            xMax: undefined,
            yMin: undefined,
            yMax: undefined
        };

    function chart(selection) {
        selection.each(function(data) {
            data.forEach(function(series) {
                series.values.forEach(function(d) {
                    d.date = new Date(d.date);
                });
                series.values.sort(function(a, b) {
                    return a.date.getTime() - b.date.getTime();
                });
            });

            var x = d3.time.scale()
                .range([0, width - margin.left - margin.right]);

            var y = d3.scale.linear(); // gotta wait for the legend first

            var xAxis = d3.svg.axis()
                .scale(x)
                .ticks(10)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");


            // selects the hierarchy if it exists or creates them.
            var self, svg, tooltip;
            if (d3.select(this).select('.chart-container').empty()) {
                self = d3.select(this).append('div').attr('class', 'chart-container').style('position', 'relative');
                svg = self.append('svg');
                svg.append('g').attr('class', 'chart');
                svg.append('g').attr('class', 'legend');
                tooltip = self.append('div').classed('tooltip hidden', true);
            } else {
                self = d3.select(this).select('.chart-container');
                svg = self.select('svg');
                tooltip = self.select('.tooltip').classed('hidden', true);
            }
            svg.attr('width', width)
                .attr('height', height);
            svg.select('g.legend').attr('transform', 'translate(0, ' + margin.top / 2 + ')');

            var legend = svg.select('g.legend');
            legend.datum(!drawsLegend ? [] : data.map(function(d) {
                    return d.name;
                }))
                .call(
                    Legend().width(width)
                    .colourScale(colourScale)
                );
            var legendHeight = legend.node().getBBox().height;

            y.range([height - margin.top - legendHeight - margin.bottom, 0]);

            x.domain([
                valueBoundaries.xMin ? valueBoundaries.xMin :
                d3.min(data, function(series) {
                    return d3.min(series.values, function(d) {
                        return d.date;
                    });
                }),
                valueBoundaries.xMax ? valueBoundaries.xMax :
                d3.max(data, function(series) {
                    return d3.max(series.values, function(d) {
                        return d.date;
                    });
                })
            ]);
            y.domain([
                valueBoundaries.yMin ? valueBoundaries.yMin :
                d3.min(data, function(series) {
                    return d3.min(series.values, function(d) {
                        return d.value;
                    });
                }),
                valueBoundaries.yMax ? valueBoundaries.yMax :
                d3.max(data, function(series) {
                    return d3.max(series.values, function(d) {
                        return d.value;
                    });
                })
            ]);

            var chart = svg.select('g.chart');
            chart.attr("transform", "translate(" + margin.left + "," + (margin.top + legendHeight) + ")");

            chart.selectAll('rect').remove();
            highlightSections.forEach(function(hs) {
                chart.insert("rect", ":first-child")
                    .attr({
                        x: x(hs.start),
                        y: 0,
                        width: x(hs.end) - x(hs.start),
                        height: height - margin.top - margin.bottom - legendHeight,
                        fill: '#ffffff'
                    });
            });

            chart.insert("rect", ":first-child")
                .attr({
                    w: 0,
                    h: 0,
                    width: width - margin.left - margin.right,
                    height: height - margin.top - margin.bottom - legendHeight,
                    fill: function() {
                        if (highlightSections.length > 0) {
                            return '#DDDDDD';
                        } else {
                            return '#ffffff';
                        }
                    }
                });



            svg.selectAll('g.axis')
                .remove();

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(" + margin.left + "," + (height - margin.bottom) + ")")
                .call(xAxis)
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", function(d) {
                    return "rotate(-45)";
                });

            chart.select('.verticalLine').remove();
            var verticalLine = chart.append('line')
                .attr({
                    'x1': 0,
                    'y1': 0,
                    'x2': 0,
                    'y2': height - margin.bottom - margin.top - legendHeight
                })
                .attr("stroke", "steelblue")
                .attr('class', 'verticalLine hidden')
                .attr('stroke-dasharray', '10,10');
            chart.select('.horizontalLine').remove();

            svg.append("g")
                .attr("class", "y axis")
                .attr("transform", "translate(" + margin.left + "," + (margin.top + legendHeight) + ")")
                .call(yAxis);

            var line = d3.svg.line()
                .x(function(d) {
                    return x(d.date);
                })
                .y(function(d) {
                    return y(d.value);
                });

            var blankLine = d3.svg.line()
                .x(function(d) {
                    return x(d.date);
                })
                .y(function(d) {
                    return height - margin.bottom - margin.top - legendHeight;
                });

            var lines = chart.selectAll('g')
                .data(data, function(series) {
                    return series.name;
                });

            lines.exit().remove();

            var linesEnter = lines.enter()
                .append('g')
                .attr('class', 'line')
                .append('path')
                .attr('d', function(d) {
                    return blankLine.interpolate(d.interpolation || interpolation)(d.values);
                });

            lines.select('path').transition().duration(400)
                .attr("d", function(d) {
                    return line.interpolate(d.interpolation || interpolation)(d.values);
                })
                .style("stroke", function(d) {
                    return colourScale(d.name);
                })
                .attr('style', function(d) {
                    return d.style || '';
                });
            // .style(function(d){
            //     return d.style || {};}
            // );

            chart.on('mouseenter', function() {
                    verticalLine.classed('hidden', false);
                    tooltip.classed('hidden', false);
                })
                .on('mousemove', function() {
                    var xPos = d3.mouse(svg.node())[0];
                    var yPos = d3.mouse(svg.node())[1];


                    verticalLine.attr("transform", function() {
                        return "translate(" + (xPos - margin.left) + ",0)";
                    });


                    // get the current date for the mouse location
                    var selectedDate = x.invert(xPos - margin.left);
                    var label = 'Time: ' + d3.time.format("%Y/%m/%d %I:%M")(selectedDate);
                    // find the interseting values for each metric

                    var values = []; // [{name:, value:], {name:, value:}, ...]
                    data.forEach(function(series) {

                        if ((selectedDate >= series.values[0].date)) { // ignore if it doesnt intercept the line
                            var index = 0;
                            while (index < series.values.length && selectedDate > series.values[index].date) {
                                index++;
                            }
                            if (index != series.values.length) {
                                var interpolate = series.interpolation || interpolation;
                                if (interpolate == 'step-after'){
                                    values.push({
                                        name: series.name,
                                        value: series.values[index - 1].value
                                    });
                                } else { // default back to linear interpolation
                                    var dx = series.values[index].date - series.values[index - 1].date;
                                    var dy = series.values[index].value - series.values[index - 1].value;
                                    var value = dy/dx * (selectedDate - series.values[index - 1].date) + series.values[index-1].value;
                                    values.push({
                                        name: series.name,
                                        value: value
                                    });
                                }
                            }
                        }
                    });

                    // order the metrics by the intersection value
                    if (values.length > 0) {
                        values.sort(function(a, b) {
                            return b.value - a.value;
                        });
                    } else {
                        // No intersections! :O
                    }

                    //add them to the label and change the tootip html
                    values.forEach(function(value) {
                        label += '<br>' + value.name + ': ' + Math.floor(value.value);
                    });
                    tooltip.html(label);

                    var tooltipX = xPos + 15;
                    if (tooltipX + tooltip.node().getBoundingClientRect().width > width) {
                        tooltipX -= tooltip.node().getBoundingClientRect().width + 30;
                    }
                    tooltip.attr('style', 'position: absolute; left:' + tooltipX + 'px; top:' + (yPos - 35) + 'px');
                })
                .on('mouseleave', function() {
                    verticalLine.classed('hidden', true);
                    tooltip.classed('hidden', true);
                });
            chart.append('rect')
                .attr({
                    x: -margin.left,
                    y: -margin.top - legendHeight,
                    width: margin.left,
                    height: height,
                    fill: '#ffffff'
                });
            chart.append('rect')
                .attr({
                    x: -margin.left,
                    y: height - margin.top - legendHeight - margin.bottom,
                    width: width,
                    height: margin.bottom,
                    fill: '#ffffff'
                });
        });
    }

    chart.margin = function(_) {
        if (!arguments.length) return margin;
        margin = _;
        return chart;
    };

    chart.width = function(_) {
        if (!arguments.length) return width;
        width = _;
        return chart;
    };

    chart.height = function(_) {
        if (!arguments.length) return height;
        height = _;
        return chart;
    };

    chart.drawsLegend = function(_) {
        if (!arguments.length) return drawsLegend;
        drawsLegend = _;
        return chart;
    };

    chart.legendRectSize = function(_) {
        if (!arguments.length) return legendRectSize;
        legendRectSize = _;
        return chart;
    };

    chart.legendSpacing = function(_) {
        if (!arguments.length) return legendSpacing;
        legendSpacing = _;
        return chart;
    };

    chart.colourScale = function(_) {
        if (!arguments.length) return colourScale;
        colourScale = _;
        return chart;
    };

    chart.xScale = function(_) {
        if (!arguments.length) return xScale;
        xScale = _;
        return chart;
    };
    chart.yScale = function(_) {
        if (!arguments.length) return yScale;
        yScale = _;
        return chart;
    };
    chart.interpolation = function(_) {
        if (!arguments.length) return interpolation;
        interpolation = _;
        return chart;
    };
    chart.highlightSections = function(_) {
        if (!arguments.length) return highlightSections;
        highlightSections = _.map(function(d) {
            return {
                start: new Date(d.start),
                end: new Date(d.end)
            }
        });
        return chart;
    };
    chart.valueBoundaries = function(_) {
        if (!arguments.length) return valueBoundaries;
        valueBoundaries = _;
        return chart;
    };

    return chart;
}

function removeDuplicateNeighbours(data, accessor) {
    /* Removes points that have a duplicate x coordinate so that steps do not
    drop back down to zero when they start and end on the same point

    Note that it assumes the values are in order (so overlapping steps are not
    dealt with here) */

    toRemove = []
    for (var i = 1; i < data.length; i++) {
        if (accessor(data[i - 1]) == accessor(data[i])) {
            toRemove.push(i - 1);
        }
    }
    for (var i = toRemove.length - 1; i >= 0; i--) {
        data.splice(toRemove[i], 1);
    }
}
