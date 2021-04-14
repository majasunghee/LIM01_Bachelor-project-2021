/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';

import {
  AppBar,
  Card,
  CardHeader,
  Grid,
  Toolbar,
  Paper,
  Button,
} from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import VolumeUpIcon from '@material-ui/icons/VolumeUp';
import ProgressBar from '../../components/ProgressBar';
import NextExerciseBtn from '../../components/NextExerciseBtn/NextExerciseBtn';
import useStyles from './styles';
import { axiosInstanceGet } from '../../helpers/ApiFunctions';

const RyddeSetninger = ({ id, showFeedback, progress, possible }) => {
  const classes = useStyles();

  const [renderPage, setRenderPage] = useState();
  const [words] = useState([]);
  const [chosenWords, setChosenWords] = useState([]);
  const [wordWithColorCode, setWordWithColorCode] = useState([]);

  const [wordClasses] = useState([]);
  const [rightAnswer, setRightAnswer] = useState();
  const [answerState, setAnswerState] = useState();
  const [disableButton, setDisableButton] = useState(false);
  const [score, setScore] = useState(0);

  let concatenatedWords = [];
  let counter = 0;

  // splits the words in the sentence from their wordclasses
  const splitData = (el) => {
    counter += 1;
    if (!(el === '' || typeof el === 'number')) {
      if (counter % 2 === 0) {
        words.push(el);
      } else {
        wordClasses.push(el);
      }
    }
  };

  const randomizeWords = () => {
    concatenatedWords.sort(() => Math.random() - 0.5);
  };

  const colorCodeTransform = (wordClass) => {
    switch (wordClass) {
      case 'det':
        return { backgroundColor: '#FDFF95' };
      case 'prp':
        return { backgroundColor: '#8EE7EF' };
      case 'pron':
        return { backgroundColor: '#9EFFFA' };
      case 'adv':
        return { backgroundColor: '#8EEF98' };
      case 'intj':
        return { backgroundColor: '#CDFFC0' };
      case 'v':
        return { backgroundColor: '#FA9D48' };
      case 'conj':
        return { backgroundColor: '#F3BB88' };
      case 'n':
        return { backgroundColor: '#EC6F6F' };
      case 'subj':
        return { backgroundColor: '#FF9E9E' };
      case 'adj':
        return { backgroundColor: '#D08EEF' };
      default:
        return { backgroundColor: '#E0E0E0' };
    }
  };

  const filterData = (data) => {
    Object.values(data).map((el) => splitData(el));
    setRightAnswer([...words]);
    concatenatedWords = words.map(function (e, i) {
      return [words[i], wordClasses[i]];
    });
    randomizeWords();
    concatenatedWords.forEach(function (item, index, array) {
      const hexCode = colorCodeTransform(item[1]);
      concatenatedWords[index].splice(1, 1, hexCode);
    });
    setWordWithColorCode([...concatenatedWords]);
  };

  function getContent() {
    axiosInstanceGet()
      .get(`/rydde_setninger/${id}`)
      .then((res) => {
        filterData(res.data);
        setRenderPage((renderPage) => renderPage + 1);
      })
      .catch((e) => {
        return e;
      });
  }

  const clicked = (e, el) => {
    chosenWords.push(el);
    const temp = [...wordWithColorCode];
    temp.splice(e.currentTarget.id, 1);
    setWordWithColorCode(temp);
  };

  const removeWord = (e, el) => {
    wordWithColorCode.push(el);
    const temp = [...chosenWords];
    temp.splice(e.currentTarget.id, 1);
    setChosenWords(temp);
  };

  const checkAnswer = () => {
    setDisableButton(true);
    const finalSentence = chosenWords.map((el) => el[0]);
    if (JSON.stringify(finalSentence) === JSON.stringify(rightAnswer)) {
      setAnswerState('correct');
      setScore(1);
    } else {
      setAnswerState('incorrect');
      setScore(0);
    }
  };

  const nextExercise = () => {
    showFeedback(score);
  };

  useEffect(() => {
    getContent();
  }, []);

  return (
    <Paper className={classes.root}>
      <AppBar className={classes.navbar} position="static">
        <ProgressBar progress={progress} possible={possible} />
        <Toolbar>
          <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="menu"
          >
            <MenuIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Paper className={classes.layout} elevation={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardHeader
                avatar={<VolumeUpIcon />}
                title="Trykk på ordene sånn at de kommer i
                 riktig rekkefølge. Husk å sjeekke tegnsettingen!"
              />
            </Card>
          </Grid>
          <Grid item xs={12}>
            <div>
              {wordWithColorCode.map((el, index) => (
                <Button
                  id={index}
                  value={el[0]}
                  style={el[1]}
                  className={classes.wordBtn}
                  variant="contained"
                  disabled={disableButton}
                  onClick={(e) => clicked(e, el)}
                >
                  {el[0]}
                </Button>
              ))}
            </div>
          </Grid>
          <Grid item xs={12}>
            <div className={classes.chosenWords}>
              {chosenWords.map((el, index) => (
                <Button
                  id={index}
                  value={el[0]}
                  style={el[1]}
                  className={classes.wordBtn}
                  variant="contained"
                  disabled={disableButton}
                  onClick={(e) => removeWord(e, el)}
                >
                  {el[0]}
                </Button>
              ))}
            </div>
          </Grid>
          <Grid item xs={6} />
          <Grid item xs={6}>
            <Button
              variant="outlined"
              style={{ backgroundColor: 'white' }}
              disabled={disableButton}
              onClick={checkAnswer}
            >
              Sjekk svar
            </Button>
          </Grid>
          <NextExerciseBtn
            answerState={answerState}
            handleNextTask={nextExercise}
          />
        </Grid>
      </Paper>
    </Paper>
  );
};

export default RyddeSetninger;
