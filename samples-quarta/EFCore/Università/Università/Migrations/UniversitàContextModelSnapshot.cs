﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Università.Data;

#nullable disable

namespace Università.Migrations
{
    [DbContext(typeof(UniversitàContext))]
    partial class UniversitàContextModelSnapshot : ModelSnapshot
    {
        protected override void BuildModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder.HasAnnotation("ProductVersion", "7.0.11");

            modelBuilder.Entity("Università.Model.Corso", b =>
                {
                    b.Property<int>("CodiceCorso")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<int?>("CodDocente")
                        .HasColumnType("INTEGER");

                    b.Property<string>("Nome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("CodiceCorso");

                    b.HasIndex("CodDocente");

                    b.ToTable("Corsi");
                });

            modelBuilder.Entity("Università.Model.CorsoLaurea", b =>
                {
                    b.Property<int>("CorsoLaureaId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("Facoltà")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("TipoLaurea")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("CorsoLaureaId");

                    b.ToTable("CorsiLaurea");
                });

            modelBuilder.Entity("Università.Model.Docente", b =>
                {
                    b.Property<int>("CodDocente")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<string>("Cognome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("Dipartimento")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<string>("Nome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("CodDocente");

                    b.ToTable("Docenti");
                });

            modelBuilder.Entity("Università.Model.Frequenta", b =>
                {
                    b.Property<int>("Matricola")
                        .HasColumnType("INTEGER");

                    b.Property<int>("CodCorso")
                        .HasColumnType("INTEGER");

                    b.HasKey("Matricola", "CodCorso");

                    b.HasIndex("CodCorso");

                    b.ToTable("Frequenze");
                });

            modelBuilder.Entity("Università.Model.Studente", b =>
                {
                    b.Property<int>("Matricola")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("INTEGER");

                    b.Property<int>("AnnoNascita")
                        .HasColumnType("INTEGER");

                    b.Property<string>("Cognome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.Property<int>("CorsoLaureaId")
                        .HasColumnType("INTEGER");

                    b.Property<string>("Nome")
                        .IsRequired()
                        .HasColumnType("TEXT");

                    b.HasKey("Matricola");

                    b.HasIndex("CorsoLaureaId");

                    b.ToTable("Studenti");
                });

            modelBuilder.Entity("Università.Model.Corso", b =>
                {
                    b.HasOne("Università.Model.Docente", "Docente")
                        .WithMany("Corsi")
                        .HasForeignKey("CodDocente");

                    b.Navigation("Docente");
                });

            modelBuilder.Entity("Università.Model.Frequenta", b =>
                {
                    b.HasOne("Università.Model.Corso", "Corso")
                        .WithMany("Frequenze")
                        .HasForeignKey("CodCorso")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("Università.Model.Studente", "Studente")
                        .WithMany("Frequenze")
                        .HasForeignKey("Matricola")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("Corso");

                    b.Navigation("Studente");
                });

            modelBuilder.Entity("Università.Model.Studente", b =>
                {
                    b.HasOne("Università.Model.CorsoLaurea", "CorsoLaurea")
                        .WithMany("Studenti")
                        .HasForeignKey("CorsoLaureaId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("CorsoLaurea");
                });

            modelBuilder.Entity("Università.Model.Corso", b =>
                {
                    b.Navigation("Frequenze");
                });

            modelBuilder.Entity("Università.Model.CorsoLaurea", b =>
                {
                    b.Navigation("Studenti");
                });

            modelBuilder.Entity("Università.Model.Docente", b =>
                {
                    b.Navigation("Corsi");
                });

            modelBuilder.Entity("Università.Model.Studente", b =>
                {
                    b.Navigation("Frequenze");
                });
#pragma warning restore 612, 618
        }
    }
}
