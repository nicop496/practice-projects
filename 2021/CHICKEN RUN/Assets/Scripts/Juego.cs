using System.Collections;
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Juego : MonoBehaviour
{
    [Range(0f, 2f)]
    public float velocidad = 0.3f;
    // Todas las demas cosas (jugador, enemigos, etc.)
    public RawImage fondo;
    public RawImage suelo;
    public GameObject GUI_Quieto;
    public GameObject jugador;
    public GameObject generadorDeEnemigos;
    private AudioSource musicaDeFondo;
    public Text textoPuntos;
    public Text textoMejorPunt;
    public GameObject GUI_puntuacion;

    // Variabless
    float cadaCuantoCambiaLaDificultad = 4f;
    float aumentoDeDificultad = .10f;
    private float puntuacion = 0;

    // Estados del juego (quieto y jugando)
    public enum GameState { Quieto, Jugando };
    public GameState gameState = GameState.Quieto;

    void Start()
    {
        musicaDeFondo = GetComponent<AudioSource>();
        textoMejorPunt.text = "Mejor punt.: " + GetMaxPunt().ToString();
    }

    // Update
    void Update()
    {
        //velocidad real de la que se mueve el fondo y el suelo
        float velocidad_real = velocidad * Time.deltaTime;
        //mover el fondo
        fondo.uvRect = new Rect(fondo.uvRect.x + velocidad_real / 6, 0f, 1f, 1f);

        // Comenzar el juego cuando se haga un click (y el estado del juego es Quieto)
        if (gameState == GameState.Quieto && Input.GetMouseButtonDown(0) && jugador.GetComponent<Jugador>().Listo)
        {
            gameState = GameState.Jugando;
            GUI_Quieto.SetActive(false);
            jugador.SendMessage("AnimacionDeCorrer");
            generadorDeEnemigos.SendMessage("IniciarGenerador");
            musicaDeFondo.Play();
            InvokeRepeating("CambiarDificultad", cadaCuantoCambiaLaDificultad, cadaCuantoCambiaLaDificultad);
            GUI_puntuacion.SetActive(true);
            puntuacion = 0;
            textoPuntos.text = "Puntuación: " + puntuacion.ToString();
        }

        //que hacer si el estado del juego es "Jugando"
        if (gameState == GameState.Jugando)
        {
            //mover el suelo
            suelo.uvRect = new Rect(suelo.uvRect.x + velocidad_real, 0f, 1f, 1f);
        }


    }
    void GameOver()
    {
        gameState = GameState.Quieto;
        musicaDeFondo.Stop();
        Time.timeScale = 1;
        CancelInvoke();
    }

    // getter y setter de la maxima puntuacion
    public int GetMaxPunt(){return PlayerPrefs.GetInt("Maxima puntuacion", 0);}
    public void SetMaxPunt(int punt) { PlayerPrefs.SetInt("Maxima puntuacion", punt); }
    

    // metodos para cambiar la puntuacion
    void subirPuntuacion(float n) { 
        puntuacion += n; textoPuntos.text = "Puntuación: " + puntuacion.ToString(); 
        if (puntuacion > GetMaxPunt())
        {
            textoMejorPunt.text = "Mejor punt.: " + Convert.ToInt32(puntuacion).ToString();
            SetMaxPunt(Convert.ToInt32(puntuacion));
        }
    }

    // metodo para cambiar la dificultad
    void CambiarDificultad() {Time.timeScale += aumentoDeDificultad;}
}




