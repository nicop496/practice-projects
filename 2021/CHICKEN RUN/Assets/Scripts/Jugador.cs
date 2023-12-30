using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Jugador : MonoBehaviour
{
    

    private Animator animacion;
    public GameObject GeneradorDeEnemigos;
    public GameObject ControladorJuego;

    //variables
    public int contadorSaltos = 0;
    public bool Listo = true;
    private int muertes = 0;

    //musica
    private AudioSource sonido;
    public AudioClip sonidoMorir;
    public AudioClip sonidoSaltar;

    // Start is called before the first frame update
    void Start()
    {
        sonido = GetComponent<AudioSource>();
        animacion = GetComponent<Animator>();
        animacion.StartPlayback();
        Listo = true;
    }
    
    // Update is called once per frame
    void Update()
    {
        // Si hay un click izquierdo:
        if (Input.GetMouseButtonDown(0) && Listo)
        {
            // el contador de saltos se incrementa en 1
            contadorSaltos++;

            /* aca el programa pregunta si el contador de saltos es 0, pero la
             * unica manera de que eso pase LUEGO de que haya un click
             * es si se produjo un game over, entonces, en otras palabras,
             * esto pregunta si hay game over y se hizo un click (o sea que
             * se quiere volver a jugar)...
             */
            if (contadorSaltos == 0) 
            {
                //...y si eso pasa, primero se cambia la animacion a la de correr,
                CambiarAnimacion("jugador_corriendo");
                //luego se inicia el generador de enemigos,
                GeneradorDeEnemigos.SendMessage("IniciarGenerador");
                //y por ultimo se incrementa en 1 el contador de saltos
                contadorSaltos++;
            }
            // saltar solo si el contador de saltos es mayor a 1
            if (contadorSaltos > 1)
            {
                CambiarAnimacion("jugador_saltando");
                if (transform.position.y < .2f)
                {
                    sonido.clip = sonidoSaltar;
                    sonido.Play();
                }
            }

        }
    }
    
    // Sobreescritura del metodo que dice que pasa con los colliders,
    // o sea que pasa si el pollo y el zorro se chocan (game over).
    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.gameObject.tag == "enemigo")
        {
            muertes++;
            Listo = false;
            Destroy(other.gameObject);//eliminar al enemigo
            GeneradorDeEnemigos.SendMessage("CancelarGeneracion");//cancelar la generacion de los enemigos
            contadorSaltos = -1;//redefinir el contador de saltos a -1
            CambiarAnimacion("jugador_muere");//cambiar la animacion del jugador a la de muerte
            ControladorJuego.SendMessage("GameOver");
            sonido.clip = sonidoMorir;
            sonido.Play();
        } else if (other.gameObject.tag == "punto") {
            if (muertes == 0){ControladorJuego.SendMessage("subirPuntuacion", 1f);}
            else{ ControladorJuego.SendMessage("subirPuntuacion",.5f); }
            
        }
    }

    void SetListo() { Listo = true; }
    void AnimacionDeCorrer(){animacion.StopPlayback();} //(sí que se usa pero en el script "Juego.cs")
    
    // Funcion para cambiar la animacion (del jugador, claro)
    public void CambiarAnimacion(string anim = null){if (anim != null){animacion.Play(anim);}}
}
