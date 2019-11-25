'use babel';

import FastNavView from './fast-nav-view';
import FastNavAlgo from './package';
import FastNavTrain from './FastNavTrain';
import FastNavTest from './FastNavTest';

import {
	CompositeDisposable
} from 'atom';

import {
	readFile,
	writeFile
} from 'fs';

import {
	dirname
} from 'path';

import trainingSequence from './training_sequence.json';
import testingSequence from './testing_sequence.json';

export default {
	fastNavView: null,
	modalPanel: null,
	subscriptions: null,

	activate(state) {
		// Events subscribed to in atom's system can be easily cleaned up with a CompositeDisposable
		this.subscriptions = new CompositeDisposable();

		// Register command that toggles this view
		this.subscriptions.add(atom.commands.add('atom-workspace', {
			'fast-nav:toggle': () => this.toggle(),
			'fast-nav:training': () => this.toggleTraining(),
			'fast-nav:testing': () => this.toggleTesting()
		}));

		global.fastNav = {
			primaryKey: false,
			secondaryKey: false,
			fastNavModule: null,
			training: false,
			fastNavView: null,
			fastNavTrain: null,
			fastNavTest: null,
			shiftPress: false,
			testing: false,
		}

		const editor = atom.workspace.getActiveTextEditor();

		if(editor == undefined){
			return;
		}
		//console.log(editor.scan(/emad/i));
		editorView = atom.views.getView(editor);

		global.fastNav.fastNavView = new FastNavView(state.fastNavViewState);
		global.fastNav.fastNavModule = new FastNavAlgo();
		global.fastNav.fastNavModule.setRowHeight(editor.lineHeightInPixels);
		global.fastNav.fastNavModule.setColumnWidth(24);

		global.fastNav.fastNavTrain = new FastNavTrain(trainingSequence);
		global.fastNav.fastNavTrain.setRowHeight(editor.lineHeightInPixels);
		global.fastNav.fastNavTrain.setColumnWidth(12.05);

		global.fastNav.fastNavTest = new FastNavTest(testingSequence);

		editorView.addEventListener('keypress', function (event) {
			if (global.fastNav.primaryKey === true) {
				if (event.code !== "Space") {
					global.fastNav.fastNavModule.RegisterKeyPress(event.code);
					if (global.fastNav.primaryKey && !(global.fastNav.secondaryKey)) {
						global.fastNav.fastNavModule.setCursorPos(editor.getCursorScreenPosition());
						const C = global.fastNav.fastNavModule.getCursorPosition("primary");
						if(C == "up"){
							editor.moveUp();
						}
						if(C == "down"){
							editor.moveDown();
						}
						if(C == "left"){
							editor.moveLeft();
						}
						if(C == "right"){
							editor.moveRight();
						}
						global.fastNav.fastNavTest.record("stroke_primary", event.code);
					}
				}
				event.preventDefault();
			} else if (global.fastNav.testing) {
				// Record Event
				const Ci = editor.getCursorScreenPosition();
				global.fastNav.fastNavTest.record("keypress", [event.code, Ci]);
			}
		}, false);

		editorView.addEventListener('keydown', function (event) {
			if (global.fastNav.testing && event.code) {
				// Record Event
				var code;
				if(event.altKey){
					// Word Jump
					if(event.code == "ArrowLeft"){
						code = "word_jump_left";
					} else if(event.code == "ArrowRight"){
						code = "word_jump_right";
					}
				} else if(event.metaKey){
					// EOL
					if(event.code == "ArrowLeft"){
						code = "bol";
					} else if(event.code == "ArrowRight"){
						code = "eol";
					}  else if(event.code == "ArrowUp"){
						code = "text_top";
					} else if(event.code == "ArrowDown"){
						code = "text_bottom";
					}
				} else{
					code = event.code;
				}

				const Ci = editor.getCursorScreenPosition();
				global.fastNav.fastNavTest.record("keypress", [code, Ci]);
			}

			//event.stopPropagation(); // to prevent modifier keys
			if (event.code === "Escape") {
				global.fastNav.primaryKey = true;
				if(global.fastNav.shiftPress){
					global.fastNav.secondaryKey = true;
					global.fastNav.fastNavModule.ClearData();
					global.fastNav.fastNavModule.setCursorPos(editor.getCursorScreenPosition());
				}
			}

			if (global.fastNav.primaryKey && event.code === "ShiftLeft") {
				global.fastNav.secondaryKey = true;
				global.fastNav.primaryKey = true;
				global.fastNav.fastNavModule.ClearData();
				global.fastNav.fastNavModule.setCursorPos(editor.getCursorScreenPosition());
			} else if(event.code === "ShiftLeft"){
				global.fastNav.shiftPress = true;
			}

			console.log(global.fastNav.shiftPress)
		}, false);

		editorView.addEventListener('keyup', function (event) {
			if (event.code === "Escape") {
				global.fastNav.primaryKey = false;
				global.fastNav.secondaryKey = false;
				global.fastNav.fastNavModule.ClearData();
			} else if (event.code === "ShiftLeft") {
				global.fastNav.secondaryKey = false;
				global.fastNav.shiftPress = false;
				const pressData = global.fastNav.fastNavModule.getKeyData();
				if (pressData.length) {
					global.fastNav.fastNavTest.record("stroke_secondary", pressData);
				}
				global.fastNav.fastNavModule.ClearData();
			}
			return;
		}, false);

		console.log("Package Activated");

		setInterval(function () {
			if (global.fastNav.secondaryKey) {
				const Cold = editor.getCursorScreenPosition();
				editor.setCursorScreenPosition(global.fastNav.fastNavModule.getCursorPosition("secondary"));
				const Cnew = editor.getCursorScreenPosition();
				const M = global.fastNav.fastNavModule.getSlope();
				if(Math.abs(Cold.column - Cnew.column) > 40){
						editor.setCursorScreenPosition(Cold);
				}
				global.fastNav.fastNavModule.setLatestCursorPos(editor.getCursorScreenPosition());
			}

			const C = editor.getCursorScreenPosition();

			// Testing Code
			if(global.fastNav.testing){
				const configPath = atom.config.getUserConfigPath();
				const atomDir = dirname(configPath);

				if (global.fastNav.fastNavTest.testComplete()) {
					global.fastNav.fastNavView.testingCompleted();
					// Save data to file
					writeFile(atomDir + "/storage/fastNav_test.txt", JSON.stringify(global.fastNav.fastNavTest.getRecordedData()), function (err) {
							if (err) console.log(err);
					});
				} else{
					global.fastNav.fastNavTest.testText(atom.workspace.getActiveTextEditor().getText());
					global.fastNav.fastNavView.activateWord(global.fastNav.fastNavTest.getWord());

					writeFile(atomDir + "/storage/fastNav_test.txt", JSON.stringify(global.fastNav.fastNavTest.getRecordedData()), function (err) {
							if (err) console.log(err);
					});
				}

			}
			// Training Code
			else if(global.fastNav.training) {
				if (global.fastNav.fastNavTrain.trainComplete()) {
					global.fastNav.fastNavView.trainingCompleted();
				} else {
					console.log(C, global.fastNav.fastNavTrain.targetCursorPosition())
					if (C.isEqual(global.fastNav.fastNavTrain.targetCursorPosition())) {
						global.fastNav.fastNavTrain.nextIndex();
					}

					global.fastNav.fastNavView.trainingActivate(global.fastNav.fastNavTrain.getMarkerPosition());
				}
			}
			else {

				global.fastNav.fastNavView.deactivate();
			}
		}, 10);
	},

	deactivate() {
		//this.modalPanel.destroy();
		this.subscriptions.dispose();
		this.fastNavView.destroy();
	},

	serialize() {
		return {
			//fastNavViewState: this.fastNavView.serialize()
		};
	},

	toggle() {
		/*
		console.log('FastNav was toggled!');
		return (
		  this.modalPanel.isVisible() ?
		  this.modalPanel.hide() :
		  this.modalPanel.show()
		);
		*/
	},

	toggleTraining() {
		if (!global.fastNav.training) {
			console.log("Training started");
			global.fastNav.training = true;
			global.fastNav.testing = false;
			global.fastNav.fastNavTrain.setDimensions(global.fastNav.fastNavView.getPageDimensions());
		} else {
			global.fastNav.training = false;
			global.fastNav.testing = false;
			global.fastNav.fastNavView.deactivate();
		}
	},

	toggleTesting() {
		if (!global.fastNav.testing) {
			console.log("Testing started");
			global.fastNav.testing = true;
			global.fastNav.training = false;
		} else {
			global.fastNav.training = false;
			global.fastNav.testing = false;
			global.fastNav.fastNavView.deactivate();
		}
	}

};
