// 2018-2020topchart.csv
// topChartWithFeatures.csv
function drawData(data) {
    console.log(data);

    let artists = new Set();
    let songs = new Set();
    data.forEach(function (d) {
        let song = d["Song"];
        let artist = d["Artist"];
        songs.add(song);
        artists.add(artist);
    });

    let width = 800;
    let height = 700;
    let margins = {
        top: 20,
        right: 20,
        bot: 50,
        left: 60
    };
    let chartWidth = width - margins.left - margins.right;
    let chartHeight = height - margins.top - margins.bot;

    //line graph
    let songLine = {};
    data.forEach(function (d) {
        let song = d["Song"];
        let artist = d["Artist"];
        let key = song + "/:/" + artist;
        if (key in songLine) {
            let date = d3.timeParse("%m/%d/%y")(d["Date"]);
            // let currDates = songLine[key];
            // let lastDate = currDates[currDates.length-1];
            // if (date != lastDate + 1){

            // }
            songLine[key].push({
                "song": song,
                "artist": artist,
                "rank": d["Rank"],
                "date": date
            })
        } else {
            let date = d3.timeParse("%m/%d/%y")(d["Date"]);
            songLine[key] = [{
                "song": song,
                "artist": artist,
                "rank": d["Rank"],
                "date": date
            }]
        }
    });
    console.log(songLine);

    let lineSvg = d3.select("#line_graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + margins.left + "," + margins.top + ")");

    songValues = Object.values(songLine)
    const firstDate = songValues[0][0]["date"];
    const lastDate = songValues[songValues.length - 1][0]["date"];
    let dateScale = d3.scaleTime()
        .domain([firstDate, lastDate])
        .range([0, chartWidth]);
    let linexAxis = lineSvg.append("g")
        .attr("transform", "translate(0," + chartHeight + ")");
    linexAxis.call(d3.axisBottom(dateScale));
    lineSvg.append("text") //x axis
        .attr("transform", "translate(" + (chartWidth / 2) + "," +
            (chartHeight + margins.top + 20) + ")")
        .style("text-anchor", "middle")
        .text("Date")

    let rankScale = d3.scaleLinear()
        .domain([1, 200])
        .range([0, chartHeight]);
    lineSvg.append("g")
        .call(d3.axisLeft(rankScale));
    lineSvg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margins.left + 10)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Rank");

    let songEntries = Object.entries(songLine);
    let color = d3.scaleOrdinal(d3.schemeAccent);
    let formatTime = d3.timeFormat("%B %d %Y");
    let tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    let clip = lineSvg.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", chartWidth)
        .attr("height", chartHeight)
        .attr("x", 0)
        .attr("y", 0);
    let line = lineSvg.append("g")
        .attr("clip-path", "url(#clip)");
    let isClicked = false;
    let brush = d3.brushX()
        .extent([
            [0, 0],
            [chartWidth, chartHeight]
        ])
        .on("end", function () {
            let extent = d3.event.selection;
            if (!extent) {
                if (!idleTimeout) return idleTimeout = setTimeout(idled, 350);
                resizeGraph(firstDate, lastDate, reset = true);
            } else {
                line.select(".brush").call(brush.move, null);
                resizeGraph(dateScale.invert(extent[0]), dateScale.invert(extent[1]), reset = false);
            }
        });
    line.append('g')
        .attr("class", "brush")
        .call(brush);

    let idleTimeout;

    function idled() {
        idleTimeout = null;
    }

    function resizeGraph(first = firstDate, last = lastDate, reset = false) {
        isClicked = true;
        if (reset) {
            lineSvg.selectAll(".line").each(function () {
                let element = d3.select(this);
                element.style("opacity", 1);
            });
        }
        dateScale.domain([first, last]);
        linexAxis.transition().duration(1000).call(d3.axisBottom(dateScale));
        line.selectAll(".line")
            .transition()
            .duration(1000)
            .attr("d", d3.line()
                .curve(d3.curveLinear)
                .x(function (d) {
                    return dateScale(d.date)
                })
                .y(function (d) {
                    return rankScale(d.rank)
                })
            )
            .on("end", function () {
                isClicked = false;
            });
    }

    function lineFilter(filter = "", filterType = "") {
        let filterData = [];
        if (filter != "") {
            songEntries.forEach(function (result) {
                let song = result[1][0].song;
                let artist = result[1][0].artist;
                if (filterType == "artist") {
                    if (artist == filter) {
                        filterData.push(result);
                    }
                } else if (filterType == "song") {
                    if (song == filter) {
                        filterData.push(result);
                    }
                }
            });
        } else {
            filterData = songEntries;
        }
        filterData.forEach(function (result) {
            let key = result[0];
            let value = result[1];
            let normalStroke = 2.5;
            line.append("path")
                .datum(value)
                .attr("class", "line")
                .attr("fill", "none")
                .attr("stroke", color(key))
                .attr("stroke-width", normalStroke)
                .attr("id", d => d[0].song + "/%/" + d[0].artist)
                .attr("d", d3.line()
                    .curve(d3.curveLinear)
                    .x(function (d) {
                        return dateScale(d.date)
                    })
                    .y(function (d) {
                        return rankScale(d.rank)
                    })
                )
                .on("click", function (d) {
                    lineSvg.selectAll(".line").each(function () {
                        let element = d3.select(this);
                        if (element.attr("id") != d[0].song + "/%/" + d[0]
                            .artist) {
                            element.style("opacity", 0.1);
                        } else {
                            element.style("opacity", 1);
                        }
                    });
                    let fDate = d[0]["date"];
                    let lDate = d[d.length - 1]["date"];
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", 0)
                        .on("end", function () {
                            tooltip.html("");
                        });
                    resizeGraph(fDate, lDate, reset = false);
                })
                .on("mouseover", function (d) {
                    if (isClicked) return;
                    let extent = d3.mouse(this);
                    let time = formatTime(dateScale.invert(extent[0]));
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("stroke-width", normalStroke * 2);
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", 0.9);
                    tooltip.html(d[0].song + "<br>by: " + d[0].artist +
                            "<br>Date: " + time)
                        .style("left", (d3.event.pageX +5) + "px")
                        .style("top", (d3.event.pageY - 10) + "px");
                })
                .on("mouseout", function (d) {
                    if (isClicked) return;
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", 0)
                        .on("end", function () {
                            tooltip.html("");
                        });
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("stroke-width", normalStroke);
                });
        });
    }

    let formSelect = document.getElementById("formSelect");
    let filterSelect = document.getElementById("filterSelect");

    function updateFilter() {
        while (filterSelect.length > 0) {
            filterSelect.remove(0);
        }
        if (formSelect.value.toLowerCase() == "artist") {
            let artistsArray = Array.from(artists).sort(function (a, b) {
                if (a.toLowerCase() < b.toLowerCase()) return -1;
                if (a.toLowerCase() > b.toLowerCase()) return 1;
                return 0;
            });
            artistsArray.forEach(function (artist) {
                let option = document.createElement("option");
                option.value = artist;
                option.innerHTML = artist;
                filterSelect.appendChild(option);
            });
        } else if (formSelect.value.toLowerCase() == "song") {
            let songsArray = Array.from(songs).sort(function (a, b) {
                if (a.toLowerCase() < b.toLowerCase()) return -1;
                if (a.toLowerCase() > b.toLowerCase()) return 1;
                return 0;
            });
            songsArray.forEach(function (song) {
                let option = document.createElement("option");
                option.value = song;
                option.innerHTML = song;
                filterSelect.appendChild(option);
            });
        }
    }
    updateFilter();
    formSelect.addEventListener("change", updateFilter);
    d3.select("#filterButton").on("click", function () {
        if (isClicked) return;
        line.selectAll(".line").remove();
        lineFilter(filter = filterSelect.value, filterType = formSelect.value.toLowerCase());
        resizeGraph(firstDate, lastDate, reset = true);
    });

    d3.select("#line_graph").on("dblclick", function () { //doubleclick
        if (isClicked) return;
        resizeGraph(firstDate, lastDate, reset = true);
    });
}
drawData(chartData);